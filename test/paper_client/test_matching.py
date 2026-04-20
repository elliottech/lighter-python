import unittest

from lighter.paper_client.order_book import OrderBookLevel
from lighter.paper_client.matching import simulate_match, validate_order
from lighter.paper_client.types import (
    PaperOrderRequest,
    PaperOrderSide,
    PaperOrderType,
)
from test.paper_client.helpers import cfg


class TestValidateOrder(unittest.TestCase):
    def test_validate_rejects_zero_size(self):
        req = PaperOrderRequest(market_id=0, side=PaperOrderSide.BUY, base_amount=0)
        with self.assertRaises(ValueError):
            validate_order(req, cfg())

    def test_validate_rejects_bad_size_decimals(self):
        req = PaperOrderRequest(market_id=0, side=PaperOrderSide.BUY, base_amount=0.001)
        with self.assertRaises(ValueError):
            validate_order(req, cfg(size_decimals=2))

    def test_validate_rejects_ioc_zero_price(self):
        req = PaperOrderRequest(
            market_id=0, side=PaperOrderSide.BUY, base_amount=0.01,
            price=0, order_type=PaperOrderType.IOC,
        )
        with self.assertRaises(ValueError):
            validate_order(req, cfg())

    def test_validate_rejects_ioc_bad_price_decimals(self):
        req = PaperOrderRequest(
            market_id=0, side=PaperOrderSide.BUY, base_amount=0.01,
            price=0.001, order_type=PaperOrderType.IOC,
        )
        with self.assertRaises(ValueError):
            validate_order(req, cfg(price_decimals=2))

class TestSimulateMatch(unittest.TestCase):
    def test_market_buy_against_empty_book(self):
        req = PaperOrderRequest(market_id=0, side=PaperOrderSide.BUY, base_amount=5.0)
        fills, remaining = simulate_match(req, asks=[], bids=[], config=cfg())
        self.assertEqual(fills, [])
        self.assertEqual(remaining, 5.0)

    def test_market_buy_partial_liquidity(self):
        req = PaperOrderRequest(market_id=0, side=PaperOrderSide.BUY, base_amount=10.0)
        asks = [OrderBookLevel("3000", "3")]
        fills, remaining = simulate_match(req, asks=asks, bids=[], config=cfg())
        self.assertEqual(len(fills), 1)
        self.assertAlmostEqual(fills[0].size, 3.0)
        self.assertAlmostEqual(remaining, 7.0)

    def test_sell_ioc_stops_below_limit(self):
        req = PaperOrderRequest(
            market_id=0, side=PaperOrderSide.SELL, base_amount=5.0,
            price=2995, order_type=PaperOrderType.IOC,
        )
        bids = [OrderBookLevel("2999", "2"), OrderBookLevel("2998", "2"), OrderBookLevel("2990", "2")]
        fills, _ = simulate_match(req, asks=[], bids=bids, config=cfg())
        self.assertEqual(len(fills), 2)
        self.assertAlmostEqual(fills[0].price, 2999)
        self.assertAlmostEqual(fills[1].price, 2998)

    def test_malformed_level_skipped(self):
        req = PaperOrderRequest(market_id=0, side=PaperOrderSide.BUY, base_amount=5.0)
        fills, remaining = simulate_match(
            req, asks=[OrderBookLevel("bad", "1"), OrderBookLevel("3000", "5")], bids=[], config=cfg(),
        )
        self.assertEqual(len(fills), 1)
        self.assertAlmostEqual(fills[0].price, 3000)
        self.assertAlmostEqual(remaining, 0.0)


if __name__ == "__main__":
    unittest.main()
