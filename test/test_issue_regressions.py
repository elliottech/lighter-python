import json
import asyncio
import importlib.metadata as importlib_metadata
from unittest.mock import AsyncMock, patch

import lighter
import pytest
import lighter.signer_client as signer_client_module
from lighter.configuration import Configuration
from lighter.rest import RESTClientObject
from lighter.models.candle import Candle
from lighter.models.resp_send_tx import RespSendTx
from lighter.models.candles import Candles
from lighter.models.account_position import AccountPosition
from lighter.models.trade import Trade
from lighter.signer_client import SignerClient
from lighter.ws_client import WsClient


def test_candle_ohlc_lowercase_fields_parse():
    candle = Candle.from_dict(
        {
            "t": 1771028220000,
            "o": 0.096567,
            "h": 0.096567,
            "l": 0.096470,
            "c": 0.096470,
            "v": 10,
            "V": 0.96504,
            "i": 14278974494,
        }
    )

    assert candle is not None
    assert candle.o == 0.096567
    assert candle.h == 0.096567
    assert candle.l == 0.096470
    assert candle.c == 0.096470


def test_candles_model_nested_candles_parse():
    response = {
        "code": 200,
        "r": "1m",
        "c": [
            {
                "t": 1771028220000,
                "o": 0.096567,
                "h": 0.096567,
                "l": 0.096470,
                "c": 0.096470,
                "v": 10,
                "V": 0.96504,
                "i": 14278974494,
            }
        ],
    }

    candles = Candles.from_dict(response)
    assert candles is not None
    assert candles.code == 200
    assert candles.c is not None
    assert len(candles.c) == 1
    assert candles.c[0].o == 0.096567
    assert candles.c[0].c == 0.096470


def test_parse_message_helper_extracts_json_dict():
    payload = json.dumps({"reason": "not_filled", "source": "engine"})
    parsed = SignerClient._try_parse_json_message(payload)
    assert parsed == {"reason": "not_filled", "source": "engine"}


def test_chain_id_inference():
    assert SignerClient._infer_chain_id("https://mainnet.zklighter.elliot.ai") == 304
    assert SignerClient._infer_chain_id("https://testnet.zklighter.elliot.ai") == 300


def test_ioc_default_order_expiry_is_normalized_to_zero():
    normalized = SignerClient._normalize_order_expiry_for_tif(
        SignerClient.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,
        SignerClient.DEFAULT_28_DAY_ORDER_EXPIRY,
    )
    assert normalized == SignerClient.DEFAULT_IOC_EXPIRY


def test_non_ioc_order_expiry_keeps_default_28_day_value():
    normalized = SignerClient._normalize_order_expiry_for_tif(
        SignerClient.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
        SignerClient.DEFAULT_28_DAY_ORDER_EXPIRY,
    )
    assert normalized == SignerClient.DEFAULT_28_DAY_ORDER_EXPIRY


def test_order_expiry_rejects_seconds_timestamp():
    with pytest.raises(ValueError, match="milliseconds"):
        SignerClient._normalize_order_expiry_for_tif(
            SignerClient.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
            1_763_031_600,
        )


def test_order_expiry_rejects_expiry_less_than_five_minutes_out():
    with patch("lighter.signer_client.time.time", return_value=1_700_000_000):
        with pytest.raises(ValueError, match="at least 5 minutes in the future"):
            SignerClient._normalize_order_expiry_for_tif(
                SignerClient.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
                1_700_000_000_000 + (4 * 60 * 1000),
            )


def test_linux_aarch64_loads_arm_shared_library():
    captured_path = None

    class FakeFunction:
        def __init__(self):
            self.argtypes = None
            self.restype = None

    class FakeLibrary:
        def __init__(self):
            self.GenerateAPIKey = FakeFunction()
            self.CreateClient = FakeFunction()
            self.CheckClient = FakeFunction()
            self.SignChangePubKey = FakeFunction()
            self.SignCreateOrder = FakeFunction()
            self.SignCreateGroupedOrders = FakeFunction()
            self.SignCancelOrder = FakeFunction()
            self.SignWithdraw = FakeFunction()
            self.SignCreateSubAccount = FakeFunction()
            self.SignCancelAllOrders = FakeFunction()
            self.SignModifyOrder = FakeFunction()
            self.SignTransfer = FakeFunction()
            self.SignCreatePublicPool = FakeFunction()
            self.SignUpdatePublicPool = FakeFunction()
            self.SignMintShares = FakeFunction()
            self.SignBurnShares = FakeFunction()
            self.SignStakeAssets = FakeFunction()
            self.SignUnstakeAssets = FakeFunction()
            self.SignUpdateLeverage = FakeFunction()
            self.CreateAuthToken = FakeFunction()
            self.SignUpdateMargin = FakeFunction()
            self.SignApproveIntegrator = FakeFunction()

    def fake_cdll(path):
        nonlocal captured_path
        captured_path = path
        return FakeLibrary()

    with patch("lighter.signer_client.platform.system", return_value="Linux"), patch(
        "lighter.signer_client.platform.machine", return_value="aarch64"
    ), patch("lighter.signer_client.ctypes.CDLL", side_effect=fake_cdll):
        loaded, temp_dir = signer_client_module.__get_shared_library()

    assert loaded is not None
    assert temp_dir is None
    assert captured_path is not None
    assert captured_path.endswith("lighter-signer-linux-arm64.so")


def test_signer_client_requests_isolated_signer_instance_per_client():
    signer_instances = []
    requested_modes = []

    class FakeSigner:
        def CreateClient(self, *args):
            return None

    class DummyApiClient:
        async def close(self):
            return None

    class DummyNonceManager:
        def next_nonce(self):
            return 255, 1

    def fake_get_signer(*, isolated=False):
        requested_modes.append(isolated)
        signer = FakeSigner()
        signer_instances.append(signer)
        return signer, None

    with patch("lighter.signer_client.get_signer", side_effect=fake_get_signer), patch(
        "lighter.signer_client.nonce_manager.nonce_manager_factory",
        return_value=DummyNonceManager(),
    ), patch("lighter.signer_client.lighter.ApiClient", return_value=DummyApiClient()), patch(
        "lighter.signer_client.lighter.TransactionApi", return_value=object()
    ), patch("lighter.signer_client.lighter.OrderApi", return_value=object()):
        first_client = SignerClient(
            url="https://testnet.zklighter.elliot.ai",
            account_index=1,
            api_private_keys={2: "abc"},
        )
        second_client = SignerClient(
            url="https://testnet.zklighter.elliot.ai",
            account_index=2,
            api_private_keys={2: "def"},
        )

    assert requested_modes == [True, True]
    assert first_client.signer is not second_client.signer


def test_sign_update_leverage_forwards_margin_mode_to_signer():
    class FakeSigner:
        def __init__(self):
            self.captured_args = None

        def SignUpdateLeverage(self, *args):
            self.captured_args = args
            return args

    fake_signer = FakeSigner()
    client = object.__new__(SignerClient)
    client.signer = fake_signer
    client.account_index = 42

    original_decode = SignerClient._SignerClient__decode_tx_info
    SignerClient._SignerClient__decode_tx_info = staticmethod(lambda result: result)
    try:
        SignerClient.sign_update_leverage(
            client,
            market_index=3,
            fraction=500,
            margin_mode=SignerClient.ISOLATED_MARGIN_MODE,
            nonce=17,
            api_key_index=9,
        )
    finally:
        SignerClient._SignerClient__decode_tx_info = original_decode

    assert fake_signer.captured_args == (3, 500, SignerClient.ISOLATED_MARGIN_MODE, 17, 9, 42)


def test_update_leverage_keeps_public_margin_mode_and_fraction_mapping():
    client = object.__new__(SignerClient)
    client.sign_update_leverage = lambda *args: (1, '{"MarginMode":1}', '0xabc', None)
    client.send_tx = AsyncMock(return_value=RespSendTx(code=200, message="ok", tx_hash="0xabc", predicted_execution_time_ms=0, volume_quota_remaining=0))

    captured = {}

    def fake_sign_update_leverage(market_index, fraction, margin_mode, nonce, api_key_index):
        captured["args"] = (market_index, fraction, margin_mode, nonce, api_key_index)
        return 1, '{"MarginMode":1}', '0xabc', None

    client.sign_update_leverage = fake_sign_update_leverage

    asyncio.run(
        SignerClient.update_leverage(
            client,
            market_index=3,
            margin_mode=SignerClient.ISOLATED_MARGIN_MODE,
            leverage=20,
            nonce=17,
            api_key_index=9,
        )
    )

    assert captured["args"] == (3, 500, SignerClient.ISOLATED_MARGIN_MODE, 17, 9)


def test_package_version_matches_distribution_metadata_when_installed():
    try:
        installed_version = importlib_metadata.version("lighter-sdk")
    except importlib_metadata.PackageNotFoundError:
        assert lighter.__version__ == "0+unknown"
        return

    assert lighter.__version__ == installed_version


def test_send_tx_sets_troubleshooting_for_invalid_public_key_errors():
    client = object.__new__(SignerClient)
    client.tx_api = AsyncMock()
    client.tx_api.send_tx.return_value = RespSendTx(
        code=21136,
        message="invalid PublicKey",
        tx_hash="0x1",
        predicted_execution_time_ms=0,
        volume_quota_remaining=0,
    )

    response = asyncio.run(SignerClient.send_tx(client, tx_type=1, tx_info='{"a":1}'))

    troubleshooting = response.additional_properties.get("troubleshooting")
    assert troubleshooting is not None
    assert "api_private_keys" in troubleshooting


def test_create_auth_token_with_expiry_adds_timestamp_to_deadline():
    class FakeSigner:
        def __init__(self):
            self.captured_args = None

        def CreateAuthToken(self, *args):
            self.captured_args = args
            return type("Result", (), {"str": "token", "err": None})()

    client = object.__new__(SignerClient)
    client.signer = FakeSigner()
    client.account_index = 42

    with patch("lighter.signer_client.decode_and_free", side_effect=lambda value: value):
        auth, error = SignerClient.create_auth_token_with_expiry(
            client,
            deadline=3600,
            timestamp=1_700_000_000,
            api_key_index=7,
        )

    assert auth == "token"
    assert error is None
    assert client.signer.captured_args == (1_700_003_600, 7, 42)


def test_create_auth_token_with_default_expiry_uses_ten_minutes():
    class FakeSigner:
        def __init__(self):
            self.captured_args = None

        def CreateAuthToken(self, *args):
            self.captured_args = args
            return type("Result", (), {"str": "token", "err": None})()

    client = object.__new__(SignerClient)
    client.signer = FakeSigner()
    client.account_index = 99

    with patch("lighter.signer_client.decode_and_free", side_effect=lambda value: value):
        SignerClient.create_auth_token_with_expiry(client, timestamp=1_700_000_000, api_key_index=5)

    assert client.signer.captured_args == (1_700_000_600, 5, 99)


def test_sign_create_order_forwards_market_index_to_signer_call():
    class FakeSigner:
        def __init__(self):
            self.captured_args = None

        def SignCreateOrder(self, *args):
            self.captured_args = args
            return args

    fake_signer = FakeSigner()
    client = object.__new__(SignerClient)
    client.signer = fake_signer
    client.account_index = 42

    original_decode = SignerClient._SignerClient__decode_tx_info
    SignerClient._SignerClient__decode_tx_info = staticmethod(lambda result: result)
    try:
        SignerClient.sign_create_order(
            client,
            market_index=2048,
            client_order_index=1,
            base_amount=100,
            price=123456,
            is_ask=False,
            order_type=SignerClient.ORDER_TYPE_LIMIT,
            time_in_force=SignerClient.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
            reduce_only=False,
            trigger_price=0,
            order_expiry=SignerClient.DEFAULT_28_DAY_ORDER_EXPIRY,
            nonce=7,
            api_key_index=5,
        )
    finally:
        SignerClient._SignerClient__decode_tx_info = original_decode

    assert fake_signer.captured_args is not None
    assert fake_signer.captured_args[0] == 2048


def test_rest_client_includes_configured_proxy_in_requests():
    class DummyResponse:
        status = 200
        reason = "OK"
        headers = {}

        async def read(self):
            return b"{}"

    class CaptureRequester:
        def __init__(self):
            self.last_kwargs = None

        async def request(self, **kwargs):
            self.last_kwargs = kwargs
            return DummyResponse()

    async def run_case():
        cfg = Configuration()
        cfg.proxy = "http://127.0.0.1:8080"
        cfg.proxy_headers = {"Proxy-Authorization": "Basic abc"}

        rest_client = RESTClientObject(cfg)
        original_pool_manager = rest_client.pool_manager
        capture = CaptureRequester()
        rest_client.pool_manager = capture

        try:
            await rest_client.request("GET", "https://example.com")
        finally:
            await original_pool_manager.close()
            if rest_client.retry_client is not None:
                await rest_client.retry_client.close()

        assert capture.last_kwargs is not None
        assert capture.last_kwargs.get("proxy") == "http://127.0.0.1:8080"
        assert capture.last_kwargs.get("proxy_headers") == {"Proxy-Authorization": "Basic abc"}

    asyncio.run(run_case())


def test_sign_withdraw_forwards_asset_route_and_amount():
    class FakeSigner:
        def __init__(self):
            self.captured_args = None

        def SignWithdraw(self, *args):
            self.captured_args = args
            return args

    fake_signer = FakeSigner()
    client = object.__new__(SignerClient)
    client.signer = fake_signer
    client.account_index = 42

    original_decode = SignerClient._SignerClient__decode_tx_info
    SignerClient._SignerClient__decode_tx_info = staticmethod(lambda result: result)
    try:
        SignerClient.sign_withdraw(
            client,
            asset_index=SignerClient.ASSET_ID_USDC,
            route_type=SignerClient.ROUTE_SPOT,
            amount=123456,
            nonce=9,
            api_key_index=7,
        )
    finally:
        SignerClient._SignerClient__decode_tx_info = original_decode

    assert fake_signer.captured_args == (
        SignerClient.ASSET_ID_USDC,
        SignerClient.ROUTE_SPOT,
        123456,
        9,
        7,
        42,
    )


def test_ws_client_replies_to_application_ping_with_pong():
    sent_messages = []

    class FakeWs:
        def send(self, message):
            sent_messages.append(json.loads(message))

    client = WsClient(order_book_ids=[0], on_order_book_update=None, on_account_update=None)
    client.on_message(FakeWs(), {"type": "ping"})

    assert sent_messages == [{"type": "pong"}]


def test_ws_client_sync_keepalive_uses_protocol_ping():
    ping_calls = []

    class FakeStopEvent:
        def __init__(self):
            self.calls = 0

        def wait(self, timeout):
            self.calls += 1
            return self.calls > 1

    class FakeWs:
        def ping(self):
            ping_calls.append("ping")

    client = WsClient(order_book_ids=[0], on_order_book_update=None, on_account_update=None)
    client._sync_keepalive_stop = FakeStopEvent()

    client._sync_keepalive(FakeWs())

    assert ping_calls == ["ping"]


def test_withdraw_raises_for_unsupported_asset_id():
    client = object.__new__(SignerClient)

    with pytest.raises(ValueError, match="Unsupported asset id"):
        asyncio.run(
            SignerClient.withdraw(
                client,
                asset_id=9999,
                route_type=SignerClient.ROUTE_SPOT,
                amount=1.0,
                nonce=1,
                api_key_index=1,
            )
        )


def test_create_market_order_keeps_price_scaling_same_for_buy_and_sell():
    client = object.__new__(SignerClient)
    client.create_order = AsyncMock(return_value=(None, None, None))

    asyncio.run(
        SignerClient.create_market_order(
            client,
            market_index=2,
            client_order_index=1,
            base_amount=100,
            avg_execution_price=1_400_000,
            is_ask=False,
            nonce=11,
            api_key_index=3,
        )
    )

    asyncio.run(
        SignerClient.create_market_order(
            client,
            market_index=2,
            client_order_index=2,
            base_amount=100,
            avg_execution_price=1_400_000,
            is_ask=True,
            nonce=12,
            api_key_index=3,
        )
    )

    first_call = client.create_order.await_args_list[0]
    second_call = client.create_order.await_args_list[1]

    assert first_call.kwargs["price"] == 1_400_000
    assert second_call.kwargs["price"] == 1_400_000


def test_create_sl_market_order_sets_price_to_trigger_price():
    client = object.__new__(SignerClient)
    client.create_order = AsyncMock(return_value=(None, None, None))

    asyncio.run(
        SignerClient.create_sl_market_order(
            client,
            market_index=9,
            client_order_index=123,
            base_amount=456,
            trigger_price=789_000,
            is_ask=True,
            reduce_only=True,
            nonce=15,
            api_key_index=2,
        )
    )

    call = client.create_order.await_args
    assert call.args[0] == 9
    assert call.args[1] == 123
    assert call.args[2] == 456
    assert call.args[3] == 789_000
    assert call.args[4] is True
    assert call.args[5] == SignerClient.ORDER_TYPE_STOP_LOSS
    assert call.args[6] == SignerClient.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL
    assert call.args[7] is True
    assert call.args[8] == 789_000
    assert call.args[9] == SignerClient.DEFAULT_IOC_EXPIRY
    assert call.kwargs["nonce"] == 15
    assert call.kwargs["api_key_index"] == 2


def test_get_market_index_symbol_map_includes_perps_and_spot():
    class Market:
        def __init__(self, market_id, symbol):
            self.market_id = market_id
            self.symbol = symbol

    class Details:
        order_book_details = [Market(0, "ETH"), Market(24, "BTC")]
        spot_order_book_details = [Market(2048, "ETH-USDC")]

    class FakeOrderApi:
        async def order_book_details(self):
            return Details()

    client = object.__new__(SignerClient)
    client.order_api = FakeOrderApi()

    mapping = asyncio.run(SignerClient.get_market_index_symbol_map(client))
    assert mapping[0] == "ETH"
    assert mapping[24] == "BTC"
    assert mapping[2048] == "ETH-USDC"


def test_get_market_index_for_symbol_is_case_insensitive():
    client = object.__new__(SignerClient)

    async def fake_map(**kwargs):
        return {0: "ETH", 24: "BTC", 2048: "ETH-USDC"}

    client.get_market_index_symbol_map = fake_map

    assert asyncio.run(SignerClient.get_market_index_for_symbol(client, "eth")) == 0
    assert asyncio.run(SignerClient.get_market_index_for_symbol(client, "ETH-USDC")) == 2048
    assert asyncio.run(SignerClient.get_market_index_for_symbol(client, "SOL")) is None


def test_sign_create_grouped_orders_forwards_grouping_type_and_order_count():
    """#72 regression: sign_create_grouped_orders must forward grouping_type and every
    order in the array to SignCreateGroupedOrders unchanged."""
    from lighter.signer_client import CreateOrderTxReq

    captured = {}

    class FakeSigner:
        def SignCreateGroupedOrders(self, grouping_type, orders_arr, count, nonce, api_key_index, account_index):
            captured["grouping_type"] = grouping_type
            captured["count"] = count
            captured["nonce"] = nonce
            captured["api_key_index"] = api_key_index
            # return a SignedTxResponse-like object with null fields so decode works
            import ctypes
            from lighter.signer_client import SignedTxResponse
            r = SignedTxResponse()
            r.txType = 7
            r.txInfo = None
            r.txHash = None
            r.messageToSign = None
            r.err = None
            return r

    client = object.__new__(SignerClient)
    client.signer = FakeSigner()
    client.account_index = 5

    orders = [CreateOrderTxReq(), CreateOrderTxReq()]

    original = SignerClient._SignerClient__decode_tx_info
    SignerClient._SignerClient__decode_tx_info = staticmethod(
        lambda result: (result.txType, None, None, None)
    )
    try:
        SignerClient.sign_create_grouped_orders(
            client,
            grouping_type=SignerClient.GROUPING_TYPE_ONE_CANCELS_THE_OTHER,
            orders=orders,
            nonce=42,
            api_key_index=7,
        )
    finally:
        SignerClient._SignerClient__decode_tx_info = original

    assert captured["grouping_type"] == SignerClient.GROUPING_TYPE_ONE_CANCELS_THE_OTHER
    assert captured["count"] == 2
    assert captured["nonce"] == 42
    assert captured["api_key_index"] == 7


def test_process_api_key_and_nonce_handles_none_response_without_attribute_error():
    class FakeNonceManager:
        def __init__(self):
            self.failure_acks = 0

        def next_nonce(self):
            return 3, 77

        def acknowledge_failure(self, api_key_index):
            self.failure_acks += 1

        def hard_refresh_nonce(self, api_key_index):
            pass

    class DummyClient:
        def __init__(self):
            self.nonce_manager = FakeNonceManager()

    @signer_client_module.process_api_key_and_nonce
    async def fake_create(self, nonce=SignerClient.DEFAULT_NONCE, api_key_index=SignerClient.DEFAULT_API_KEY_INDEX):
        return None, None, "some signer error"

    client = DummyClient()
    created_tx, ret, err = asyncio.run(fake_create(client))

    assert created_tx is None
    assert ret is None
    assert err == "some signer error"
    assert client.nonce_manager.failure_acks == 1


def test_create_sl_market_order_limited_slippage_uses_adjusted_price():
    client = object.__new__(SignerClient)
    client.create_sl_order = AsyncMock(return_value=(None, None, None))

    asyncio.run(
        SignerClient.create_sl_market_order_limited_slippage(
            client,
            market_index=7,
            client_order_index=99,
            base_amount=1000,
            trigger_price=1_000_000,
            max_slippage=0.01,
            is_ask=False,
            reduce_only=True,
            ideal_price=1_000_000,
            nonce=4,
            api_key_index=6,
        )
    )

    call = client.create_sl_order.await_args
    assert call.kwargs["price"] == 1_010_000
    assert call.kwargs["trigger_price"] == 1_000_000


def test_create_tp_market_order_limited_slippage_uses_adjusted_price():
    client = object.__new__(SignerClient)
    client.create_tp_order = AsyncMock(return_value=(None, None, None))

    asyncio.run(
        SignerClient.create_tp_market_order_limited_slippage(
            client,
            market_index=7,
            client_order_index=100,
            base_amount=1000,
            trigger_price=1_000_000,
            max_slippage=0.02,
            is_ask=True,
            reduce_only=True,
            ideal_price=1_000_000,
            nonce=5,
            api_key_index=6,
        )
    )

    call = client.create_tp_order.await_args
    assert call.kwargs["price"] == 980_000
    assert call.kwargs["trigger_price"] == 1_000_000


def test_account_position_parses_optional_leverage_field():
    parsed = AccountPosition.from_dict(
        {
            "market_id": 0,
            "symbol": "ETH",
            "initial_margin_fraction": "1000",
            "open_order_count": 1,
            "pending_order_count": 1,
            "position_tied_order_count": 0,
            "sign": 1,
            "position": "1.0",
            "avg_entry_price": "2000",
            "position_value": "2000",
            "unrealized_pnl": "10",
            "realized_pnl": "0",
            "liquidation_price": "1500",
            "total_funding_paid_out": "0",
            "margin_mode": 1,
            "leverage": 20,
            "allocated_margin": "100",
            "total_discount": "0",
        }
    )

    assert parsed is not None
    assert parsed.leverage == 20


def test_signer_client_applies_proxy_to_configuration():
    captured_config = None

    class DummyApiClient:
        async def close(self):
            return None

    class DummyNonceManager:
        def next_nonce(self):
            return 255, 1

    class FakeSigner:
        def CreateClient(self, *args):
            return None

    def fake_api_client_factory(configuration):
        nonlocal captured_config
        captured_config = configuration
        return DummyApiClient()

    with patch("lighter.signer_client.get_signer", return_value=(FakeSigner(), None)), patch(
        "lighter.signer_client.nonce_manager.nonce_manager_factory",
        return_value=DummyNonceManager(),
    ), patch("lighter.signer_client.lighter.ApiClient", side_effect=fake_api_client_factory), patch(
        "lighter.signer_client.lighter.TransactionApi", return_value=object()
    ), patch("lighter.signer_client.lighter.OrderApi", return_value=object()), patch(
        "lighter.signer_client.lighter.AccountApi", return_value=object()
    ):
        SignerClient(
            url="https://testnet.zklighter.elliot.ai",
            account_index=1,
            api_private_keys={2: "abc"},
            proxy="http://127.0.0.1:8080",
            proxy_headers={"Proxy-Authorization": "Basic xyz"},
        )

    assert captured_config is not None
    assert captured_config.proxy == "http://127.0.0.1:8080"
    assert captured_config.proxy_headers == {"Proxy-Authorization": "Basic xyz"}


def test_fetch_order_checks_active_then_inactive_orders():
    class OrderObj:
        def __init__(self, order_id, client_order_index):
            self.order_id = order_id
            self.client_order_index = client_order_index

    class OrdersResp:
        def __init__(self, orders):
            self.orders = orders

    class FakeOrderApi:
        async def account_active_orders(self, **kwargs):
            return OrdersResp([OrderObj("a", 1)])

        async def account_inactive_orders(self, **kwargs):
            return OrdersResp([OrderObj("b", 2)])

    client = object.__new__(SignerClient)
    client.account_index = 77
    client.order_api = FakeOrderApi()

    found = asyncio.run(SignerClient.fetch_order(client, order_id="b"))
    assert found is not None
    assert found.client_order_index == 2


def test_fetch_positions_and_get_leverage_info():
    class Position:
        def __init__(self, market_id, initial_margin_fraction, margin_mode):
            self.market_id = market_id
            self.initial_margin_fraction = initial_margin_fraction
            self.margin_mode = margin_mode

    class Account:
        def __init__(self):
            self.positions = [Position(0, "500", 1)]

    class AccountsResp:
        def __init__(self):
            self.accounts = [Account()]

    class Market:
        def __init__(self, market_id, min_initial_margin_fraction):
            self.market_id = market_id
            self.min_initial_margin_fraction = min_initial_margin_fraction

    class MarketResp:
        def __init__(self):
            self.order_book_details = [Market(0, "250")]

    class FakeAccountApi:
        async def account(self, **kwargs):
            return AccountsResp()

    class FakeOrderApi:
        async def order_book_details(self):
            return MarketResp()

    client = object.__new__(SignerClient)
    client.account_index = 7
    client.account_api = FakeAccountApi()
    client.order_api = FakeOrderApi()

    positions = asyncio.run(SignerClient.fetch_positions(client))
    assert len(positions) == 1

    leverage = asyncio.run(SignerClient.get_leverage_info(client))
    assert 0 in leverage
    assert leverage[0]["leverage"] == 20
    assert leverage[0]["max_leverage"] == 40
    assert leverage[0]["margin_mode"] == 1


def test_trade_model_allows_nullable_margin_fraction_fields():
    trade = Trade.from_dict(
        {
            "trade_id": 1,
            "tx_hash": "0xabc",
            "type": "trade",
            "market_id": 0,
            "size": "1",
            "price": "2000",
            "usd_amount": "2000",
            "ask_id": 10,
            "bid_id": 11,
            "ask_client_id": 12,
            "bid_client_id": 13,
            "ask_account_id": 14,
            "bid_account_id": 15,
            "is_maker_ask": True,
            "block_height": 16,
            "timestamp": 17,
            "taker_fee": 18,
            "taker_position_size_before": "0",
            "taker_entry_quote_before": "0",
            "taker_initial_margin_fraction_before": None,
            "taker_position_sign_changed": False,
            "maker_fee": 19,
            "maker_position_size_before": "0",
            "maker_entry_quote_before": "0",
            "maker_initial_margin_fraction_before": None,
            "maker_position_sign_changed": False,
            "transaction_time": 20,
            "ask_account_pnl": "0",
            "bid_account_pnl": "0",
        }
    )

    assert trade is not None
    assert trade.taker_initial_margin_fraction_before is None
    assert trade.maker_initial_margin_fraction_before is None
