import unittest

from lighter.paper_client.accounting import apply_fill
from lighter.paper_client import (
    AccountTier,
    PaperClient,
    PaperHealthStatus,
    PaperOrderRequest,
    PaperOrderSide,
    PaperOrderType,
)
from test.paper_client.helpers import FakeOrderApi, book, default_detail


class TestPaperClient(unittest.IsolatedAsyncioTestCase):
    async def test_track_market_snapshot_and_market_buy_then_sell(self) -> None:
        order_api = FakeOrderApi()
        order_api.books[0] = book(
            asks=[("3000.00", "0.5"), ("3001.00", "2.0")],
            bids=[("2999.00", "0.5"), ("2998.00", "2.0")],
        )
        client = PaperClient(None, 5000.0, order_api=order_api)

        await client.track_market_snapshot(0)

        buy_result = await client.create_paper_order(
            PaperOrderRequest(
                market_id=0,
                side=PaperOrderSide.BUY,
                base_amount=1.0,
            )
        )

        self.assertAlmostEqual(buy_result.filled_size, 1.0)
        self.assertAlmostEqual(buy_result.unfilled, 0.0)
        self.assertEqual(len(buy_result.fills), 2)
        self.assertAlmostEqual(buy_result.avg_price, 3000.5)
        self.assertAlmostEqual(buy_result.quote_amount, 3000.5)
        self.assertAlmostEqual(buy_result.total_fee, 0.0)

        position = client.get_position(0)
        self.assertIsNotNone(position)
        self.assertAlmostEqual(position.size, 1.0)

        sell_result = await client.create_paper_order(
            PaperOrderRequest(
                market_id=0,
                side=PaperOrderSide.SELL,
                base_amount=1.0,
            )
        )

        self.assertAlmostEqual(sell_result.filled_size, 1.0)
        self.assertIsNone(client.get_position(0))
        self.assertEqual(len(client.get_trades()), 4)

    async def test_ioc_order_partially_fills_until_limit_price(self) -> None:
        order_api = FakeOrderApi()
        order_api.books[0] = book(
            asks=[("3000.00", "0.5"), ("3010.00", "2.0")],
            bids=[("2999.00", "1.0")],
        )
        client = PaperClient(None, 5000.0, order_api=order_api)
        await client.track_market_snapshot(0)

        result = await client.create_paper_order(
            PaperOrderRequest(
                market_id=0,
                side=PaperOrderSide.BUY,
                base_amount=2.0,
                price=3005.00,
                order_type=PaperOrderType.IOC,
            )
        )

        self.assertAlmostEqual(result.filled_size, 0.5)
        self.assertAlmostEqual(result.unfilled, 1.5)
        self.assertEqual(len(result.fills), 1)

    async def test_health_uses_cross_margin_across_markets(self) -> None:
        order_api = FakeOrderApi()
        order_api.details[1] = default_detail(1, "BTC")
        order_api.details[1].last_trade_price = 60000.0
        order_api.details[1].min_base_amount = "0.0001"
        order_api.books[0] = book(
            asks=[("3000.00", "10.0")],
            bids=[("2999.00", "10.0")],
        )
        order_api.books[1] = book(
            asks=[("60000.00", "10.0")],
            bids=[("59999.00", "10.0")],
        )
        client = PaperClient(None, 10000.0, order_api=order_api)
        await client.track_market_snapshot(0)
        await client.track_market_snapshot(1)

        await client.create_paper_order(
            PaperOrderRequest(0, PaperOrderSide.BUY, 1.0)
        )
        await client.create_paper_order(
            PaperOrderRequest(1, PaperOrderSide.BUY, 0.1)
        )

        self.assertAlmostEqual(client.get_position(0).size, 1.0)
        self.assertAlmostEqual(client.get_position(1).size, 0.1)

        health = client.get_health()
        self.assertEqual(health.status, PaperHealthStatus.HEALTHY)
        self.assertGreater(health.leverage, 0)
        self.assertLess(health.leverage, 2)

    async def test_order_can_trigger_cross_market_liquidation(self) -> None:
        order_api = FakeOrderApi()
        order_api.details[1] = default_detail(1, "BTC")
        order_api.details[1].maintenance_margin_fraction = 500
        order_api.details[1].closeout_margin_fraction = 250
        order_api.details[1].taker_fee = "0"
        order_api.details[1].min_base_amount = "0.0001"
        order_api.books[0] = book(
            asks=[("1.00", "10.0")],
            bids=[("0.99", "10.0")],
        )
        order_api.books[1] = book(
            asks=[("31.00", "10.0")],
            bids=[("30.00", "10.0")],
        )
        client = PaperClient(None, 350.0, order_api=order_api)
        await client.track_market_snapshot(0)
        await client.track_market_snapshot(1)

        apply_fill(client.account, 1, PaperOrderSide.BUY, 5.0, 100.0, 0)

        result = await client.create_paper_order(
            PaperOrderRequest(
                market_id=0,
                side=PaperOrderSide.BUY,
                base_amount=10.0,
                price=0.50,
                order_type=PaperOrderType.IOC,
            )
        )

        self.assertIsNotNone(result)
        self.assertIsNone(client.get_position(0))
        self.assertIsNone(client.get_position(1))

    async def test_request_market_liquidation_clears_position(self) -> None:
        order_api = FakeOrderApi()
        order_api.details[0].maintenance_margin_fraction = 500
        order_api.details[0].closeout_margin_fraction = 250
        order_api.details[0].taker_fee = "0"
        order_api.books[0] = book(
            asks=[("10.00", "10.0")],
            bids=[("9.00", "10.0")],
        )
        client = PaperClient(None, 5.0, order_api=order_api)
        await client.track_market_snapshot(0)
        apply_fill(client.account, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)

        result = await client.create_paper_order(
            PaperOrderRequest(0, PaperOrderSide.BUY, 0.1)
        )

        self.assertIsNotNone(result)
        self.assertIsNone(client.get_position(0))
        self.assertTrue(client.get_health().has_been_liquidated)

    async def test_mark_price_fallback_to_last_trade_price(self) -> None:
        order_api = FakeOrderApi()
        order_api.books[0] = book(asks=[], bids=[])
        client = PaperClient(None, 10000.0, order_api=order_api)
        await client.track_market_snapshot(0)

        apply_fill(client.account, 0, PaperOrderSide.BUY, 1.0, 3000.0, 0.0)

        self.assertAlmostEqual(client.get_portfolio_value(), 10000.0)

    async def test_refresh_order_book_updates_unrealized_pnl(self) -> None:
        order_api = FakeOrderApi()
        order_api.books[0] = book(
            asks=[("3000.00", "2.0")],
            bids=[("2999.00", "2.0")],
        )
        client = PaperClient(None, 10000.0, order_api=order_api)
        await client.track_market_snapshot(0)

        await client.create_paper_order(PaperOrderRequest(0, PaperOrderSide.BUY, 1.0))

        order_api.books[0] = book(
            asks=[("3100.00", "2.0")],
            bids=[("3099.00", "2.0")],
        )
        await client.refresh_order_book(0)

        position = client.get_position(0)
        self.assertIsNotNone(position)
        self.assertAlmostEqual(position.unrealized_pnl, 99.5)

    async def test_premium_tier_applies_fees(self) -> None:
        order_api = FakeOrderApi()
        order_api.books[0] = book(
            asks=[("3000.00", "0.5"), ("3001.00", "2.0")],
            bids=[("2999.00", "0.5"), ("2998.00", "2.0")],
        )
        client = PaperClient(
            None, 5000.0, order_api=order_api, account_tier=AccountTier.PREMIUM
        )
        await client.track_market_snapshot(0)

        result = await client.create_paper_order(
            PaperOrderRequest(
                market_id=0,
                side=PaperOrderSide.BUY,
                base_amount=1.0,
            )
        )

        # premium taker fee = 280 / 1_000_000 = 0.000280
        # fill 1: 0.5 * 3000 * 0.000280 = 0.42
        # fill 2: 0.5 * 3001 * 0.000280 = 0.42014
        expected_fee = 0.5 * 3000 * 0.000280 + 0.5 * 3001 * 0.000280
        self.assertAlmostEqual(result.total_fee, expected_fee, places=8)

    def test_default_tier_is_standard(self) -> None:
        client = PaperClient(None, 5000.0, order_api=FakeOrderApi())
        self.assertEqual(client._account_tier, AccountTier.STANDARD)

    async def test_repeated_orders_produce_identical_fills(self) -> None:
        order_api = FakeOrderApi()
        order_api.books[0] = book(
            asks=[("3000.00", "0.5"), ("3001.00", "2.0")],
            bids=[("2999.00", "1.0")],
        )
        client = PaperClient(None, 50000.0, order_api=order_api)
        await client.track_market_snapshot(0)

        result1 = await client.create_paper_order(
            PaperOrderRequest(0, PaperOrderSide.BUY, 1.0)
        )
        result2 = await client.create_paper_order(
            PaperOrderRequest(0, PaperOrderSide.BUY, 1.0)
        )

        self.assertAlmostEqual(result1.filled_size, result2.filled_size)
        self.assertAlmostEqual(result1.avg_price, result2.avg_price)
        self.assertAlmostEqual(result1.total_fee, result2.total_fee)


if __name__ == "__main__":
    unittest.main()
