import asyncio
from threading import RLock
from typing import Any, Dict, List, Mapping, Optional

from lighter.api.order_api import OrderApi
from lighter.api_client import ApiClient
from lighter.configuration import Configuration
from lighter.models.perps_order_book_detail import PerpsOrderBookDetail
from lighter.paper_client.order_book import InMemoryOrderBook
from lighter.paper_client.accounting import (
    copy_account,
    copy_position,
    new_paper_account,
    compute_total_account_value,
    apply_fill,
)
from lighter.paper_client.live import PaperOrderBookListener
from lighter.paper_client.matching import simulate_match, validate_order
from lighter.paper_client.risk import (
    check_and_liquidate,
    compute_health,
    compute_liquidation_price,
    update_position_metrics,
)
from lighter.paper_client.types import (
    AccountTier,
    MarketConfig,
    PaperAccount,
    PaperAccountHealth,
    PaperOrderRequest,
    PaperOrderResult,
    PaperPosition,
    PaperTrade,
    utc_now,
)


class PaperClient:
    """Local simulation client for testing trading strategies against real Lighter order book data.

    Maintains a virtual account with simulated collateral, executes taker-only fills
    against live or snapshot order book state, and tracks positions, PnL, and account
    health locally.

    Limitations:
        - Perp markets only — spot markets are not supported.
        - Taker-only — supports MARKET and IOC order types, no resting limit orders.
        - Cross-margin only — isolated margin is not simulated.
        - No funding simulation — funding rate payments are not applied to positions.
        - Read-only simulation — no transactions are submitted to the exchange; all state is local.
    """

    def __init__(
        self,
        api_client: Optional[ApiClient],
        initial_collateral_usdc: float,
        *,
        order_book_limit: int = 100,
        order_api: Optional[OrderApi] = None,
        ws_url: Optional[str] = None,
        ws_path: str = "/stream",
        initial_snapshot_timeout: float = 10.0,
        account_tier: AccountTier = AccountTier.STANDARD,
    ) -> None:
        if initial_collateral_usdc <= 0:
            raise ValueError(
                "initial collateral must be positive, "
                f"got {initial_collateral_usdc}"
            )
        if order_book_limit < 1 or order_book_limit > 250:
            raise ValueError("order_book_limit must be between 1 and 250")

        self._account_tier = account_tier

        self.api_client = api_client
        self.order_api = order_api if order_api is not None else OrderApi(api_client)
        self.order_book_limit = order_book_limit
        self.account = new_paper_account(initial_collateral_usdc)
        self.market_configs: Dict[int, MarketConfig] = {}
        self.order_books: Dict[int, InMemoryOrderBook] = {}
        raw_ws_url = ws_url if ws_url is not None else self._default_ws_url(api_client, ws_path)
        separator = "&" if "?" in raw_ws_url else "?"
        self.ws_url = f"{raw_ws_url}{separator}encoding=json"
        self.initial_snapshot_timeout = initial_snapshot_timeout
        self._live_listeners: Dict[int, PaperOrderBookListener] = {}
        self._state_lock = asyncio.Lock()
        self._state_snapshot_lock = RLock()

    async def track_market_snapshot(self, market_id: int) -> None:
        self._validate_perp_market_id(market_id)
        await self._ensure_market_config(market_id)
        await self.refresh_order_book(market_id)

    async def track_market(self, market_id: int) -> None:
        self._validate_perp_market_id(market_id)
        await self._ensure_market_config(market_id)

        if market_id in self._live_listeners:
            return

        self.order_books.setdefault(market_id, InMemoryOrderBook())
        listener = PaperOrderBookListener(
            market_id,
            self.ws_url,
            self._handle_live_order_book_message,
            initial_snapshot_timeout=self.initial_snapshot_timeout,
        )
        self._live_listeners[market_id] = listener
        try:
            await listener.start()
        except Exception:
            self._live_listeners.pop(market_id, None)
            raise

    async def stop_tracking(self, market_id: int) -> None:
        listener = self._live_listeners.pop(market_id, None)
        if listener is not None:
            await listener.stop()

    async def close(self) -> None:
        listeners = list(self._live_listeners.values())
        self._live_listeners.clear()
        await asyncio.gather(
            *(listener.stop() for listener in listeners),
            return_exceptions=True,
        )

    async def refresh_order_book(self, market_id: int) -> None:
        if market_id not in self.market_configs:
            raise ValueError(f"market {market_id} not tracked")

        snapshot = await self.order_api.order_book_orders(
            market_id=market_id,
            limit=self.order_book_limit,
        )
        async with self._state_lock:
            with self._state_snapshot_lock:
                book = self.order_books.get(market_id)
                if book is None:
                    book = InMemoryOrderBook()
                    self.order_books[market_id] = book

                book.apply_snapshot(snapshot)
                self._check_liquidation_and_update_metrics()

    async def create_paper_order(
        self,
        request: PaperOrderRequest,
    ) -> PaperOrderResult:
        async with self._state_lock:
            with self._state_snapshot_lock:
                config = self.market_configs.get(request.market_id)
                if config is None:
                    raise ValueError(
                        f"market {request.market_id} not tracked, "
                        "call track_market or track_market_snapshot first"
                    )

                book = self.order_books.get(request.market_id)
                if book is None:
                    raise ValueError(f"no order book for market {request.market_id}")

                validate_order(request, config)
                fills, unfilled = simulate_match(
                    request, list(book.asks), list(book.bids), config
                )

                total_filled_size = 0.0
                total_quote = 0.0
                total_fee = 0.0
                for fill in fills:
                    apply_fill(
                        self.account,
                        request.market_id,
                        request.side,
                        fill.size,
                        fill.price,
                        fill.fee,
                    )
                    total_filled_size += fill.size
                    total_quote += fill.size * fill.price
                    total_fee += fill.fee

                avg_price = (
                    total_quote / total_filled_size if total_filled_size > 0 else 0.0
                )
                self._check_liquidation_and_update_metrics()

                return PaperOrderResult(
                    order_type=request.order_type,
                    side=request.side,
                    market_id=request.market_id,
                    fills=fills,
                    filled_size=total_filled_size,
                    avg_price=avg_price,
                    total_fee=total_fee,
                    quote_amount=total_quote,
                    unfilled=unfilled,
                    timestamp=utc_now(),
                )

    def get_health(self) -> PaperAccountHealth:
        with self._state_snapshot_lock:
            return compute_health(
                self.account,
                self._get_mark_prices(),
                self.market_configs,
            )

    def get_liquidation_price(self, market_id: int) -> float:
        with self._state_snapshot_lock:
            return compute_liquidation_price(
                self.account,
                market_id,
                self._get_mark_prices(),
                self.market_configs,
            )

    def get_position(self, market_id: int) -> Optional[PaperPosition]:
        with self._state_snapshot_lock:
            return copy_position(self.account.positions.get(market_id))

    def get_account(self) -> PaperAccount:
        with self._state_snapshot_lock:
            return copy_account(self.account)

    def get_collateral(self) -> float:
        with self._state_snapshot_lock:
            return self.account.collateral

    def get_trades(self) -> List[PaperTrade]:
        with self._state_snapshot_lock:
            return list(self.account.trades)

    def get_portfolio_value(self) -> float:
        with self._state_snapshot_lock:
            mark_prices = self._get_mark_prices()
            if self.account.positions and not mark_prices:
                raise ValueError("no mark prices available")
            return compute_total_account_value(self.account, mark_prices)

    async def _handle_live_order_book_message(
        self,
        market_id: int,
        order_book: Mapping[str, Any],
        is_snapshot: bool,
    ) -> None:
        async with self._state_lock:
            with self._state_snapshot_lock:
                book = self.order_books.setdefault(market_id, InMemoryOrderBook())
                if is_snapshot:
                    book.apply_snapshot(order_book)
                else:
                    book.apply_delta(order_book)
                self._check_liquidation_and_update_metrics()

    def _check_liquidation_and_update_metrics(self) -> List[int]:
        liquidated_markets = check_and_liquidate(
            self.account,
            self._get_mark_prices(),
            self.market_configs,
        )
        update_position_metrics(
            self.account,
            self._get_mark_prices(),
            self.market_configs,
        )
        return liquidated_markets

    def _get_mark_prices(self) -> Dict[int, float]:
        prices: Dict[int, float] = {}
        for market_id, book in self.order_books.items():
            mark_price = book.mid_price
            if mark_price is None:
                config = self.market_configs.get(market_id)
                if config is not None and config.last_trade_price > 0:
                    mark_price = config.last_trade_price
            if mark_price is not None and mark_price > 0:
                prices[market_id] = mark_price
        return prices

    def _update_position_metrics(self) -> None:
        update_position_metrics(
            self.account,
            self._get_mark_prices(),
            self.market_configs,
        )

    async def _ensure_market_config(self, market_id: int) -> None:
        if market_id not in self.market_configs:
            await self._fetch_market_config(market_id)

    async def _fetch_market_config(self, market_id: int) -> None:
        details = await self.order_api.order_book_details(market_id=market_id)
        for detail in details.order_book_details:
            if detail.market_id != market_id:
                continue
            with self._state_snapshot_lock:
                self.market_configs[market_id] = self._market_config_from_detail(
                    detail, self._account_tier
                )
            return
        raise ValueError(f"perps order book detail not found for market {market_id}")

    @staticmethod
    def _market_config_from_detail(
        detail: PerpsOrderBookDetail,
        tier: AccountTier,
    ) -> MarketConfig:
        if detail.market_type != "perp":
            raise ValueError(
                "paper trading only supports perp markets, "
                f"got {detail.market_type!r}"
            )
        return MarketConfig(
            market_id=detail.market_id,
            symbol=detail.symbol,
            size_decimals=detail.size_decimals,
            price_decimals=detail.price_decimals,
            default_initial_margin_fraction=detail.default_initial_margin_fraction,
            min_initial_margin_fraction=detail.min_initial_margin_fraction,
            maintenance_margin_fraction=detail.maintenance_margin_fraction,
            closeout_margin_fraction=detail.closeout_margin_fraction,
            taker_fee=tier.taker_fee,
            maker_fee=tier.maker_fee,
            min_base_amount=float(detail.min_base_amount),
            min_quote_amount=float(detail.min_quote_amount),
            last_trade_price=float(detail.last_trade_price),
        )

    @staticmethod
    def _default_ws_url(api_client: Optional[ApiClient], ws_path: str) -> str:
        if api_client is not None:
            http_url = api_client.configuration.host
        else:
            http_url = Configuration.get_default().host

        if http_url.startswith("https://"):
            ws_url = "wss://" + http_url[len("https://") :]
        elif http_url.startswith("http://"):
            ws_url = "ws://" + http_url[len("http://") :]
        elif http_url.startswith("wss://") or http_url.startswith("ws://"):
            ws_url = http_url
        else:
            ws_url = "wss://" + http_url

        return f"{ws_url.rstrip('/')}/{ws_path.lstrip('/')}"

    @staticmethod
    def _validate_perp_market_id(market_id: int) -> None:
        if market_id >= 2048:
            raise ValueError(
                "paper trading only supports perp markets "
                f"(market_id < 2048), got {market_id}"
            )
