from lighter.models.market_config import MarketConfig as SdkMarketConfig
from lighter.models.order_book_details import OrderBookDetails
from lighter.models.order_book_orders import OrderBookOrders
from lighter.models.perps_order_book_detail import PerpsOrderBookDetail
from lighter.models.simple_order import SimpleOrder
from lighter.paper_client.types import MarketConfig


class FakeOrderApi:
    def __init__(self) -> None:
        self.details = {0: default_detail(0, "ETH"), 1: default_detail(1, "BTC")}
        self.books = {}

    async def order_book_details(self, market_id=None, **kwargs):
        detail = self.details[market_id]
        return OrderBookDetails(
            code=0,
            order_book_details=[detail],
            spot_order_book_details=[],
        )

    async def order_book_orders(self, market_id, limit, **kwargs):
        return self.books[market_id]


def default_detail(
    market_id: int,
    symbol: str,
    last_trade_price: float = 3000.0,
) -> PerpsOrderBookDetail:
    return PerpsOrderBookDetail(
        symbol=symbol,
        market_id=market_id,
        market_type="perp",
        base_asset_id=market_id,
        quote_asset_id=0,
        status="active",
        taker_fee="0.0005",
        maker_fee="0",
        liquidation_fee="0",
        min_base_amount="0.001",
        min_quote_amount="1.0",
        order_quote_limit="1000000",
        supported_size_decimals=4,
        supported_price_decimals=2,
        supported_quote_decimals=6,
        size_decimals=4,
        price_decimals=2,
        quote_multiplier=1,
        default_initial_margin_fraction=1000,
        min_initial_margin_fraction=500,
        maintenance_margin_fraction=50,
        closeout_margin_fraction=25,
        last_trade_price=last_trade_price,
        daily_trades_count=0,
        daily_base_token_volume=0,
        daily_quote_token_volume=0,
        daily_price_low=0,
        daily_price_high=0,
        daily_price_change=0,
        open_interest=0,
        daily_chart={},
        market_config=SdkMarketConfig(
            market_margin_mode=0,
            insurance_fund_account_index=0,
            liquidation_mode=0,
            force_reduce_only=False,
            trading_hours="",
            funding_fee_discounts_enabled=False,
            hidden=False,
            rfq_enabled=False,
        ),
        strategy_index=0,
        is_maker_fee_enabled=True,
        is_taker_fee_enabled=True,
        funding_clamp_small="0",
        funding_clamp_big="0",
        base_interest_rate="0",
    )


def cfg(market_id=0, imf=1000, mmf=500, comf=250, **kw) -> MarketConfig:
    return MarketConfig(
        market_id=market_id,
        symbol=kw.get("symbol", f"MKT{market_id}"),
        size_decimals=kw.get("size_decimals", 4),
        price_decimals=kw.get("price_decimals", 2),
        default_initial_margin_fraction=imf,
        min_initial_margin_fraction=imf,
        maintenance_margin_fraction=mmf,
        closeout_margin_fraction=comf,
        taker_fee=kw.get("taker_fee", 0.0005),
        maker_fee=kw.get("maker_fee", 0.0002),
        min_base_amount=kw.get("min_base_amount", 0.001),
        min_quote_amount=kw.get("min_quote_amount", 1.0),
        last_trade_price=kw.get("last_trade_price", 100.0),
    )


def book(asks, bids) -> OrderBookOrders:
    def _order(index, price, size):
        return SimpleOrder(
            order_index=index,
            order_id=f"order-{index}",
            owner_account_index=10,
            initial_base_amount=size,
            remaining_base_amount=size,
            price=price,
            order_expiry=0,
            transaction_time=0,
        )

    return OrderBookOrders(
        code=0,
        total_asks=len(asks),
        asks=[
            _order(index, price, size)
            for index, (price, size) in enumerate(asks, start=1)
        ],
        total_bids=len(bids),
        bids=[
            _order(index, price, size)
            for index, (price, size) in enumerate(bids, start=100)
        ],
    )
