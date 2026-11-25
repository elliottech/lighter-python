import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from lighter.signer_client import SignerClient

SIZE_ERROR = "Cannot be sure slippage will be acceptable due to the high size"


def order(price, size):
    return SimpleNamespace(price=price, remaining_base_amount=size)


def client_with_book(asks, bids):
    client = SignerClient.__new__(SignerClient)
    client.order_api = MagicMock()
    client.order_api.order_book_orders = AsyncMock(return_value=SimpleNamespace(asks=asks, bids=bids))
    client.create_order = AsyncMock(return_value=("tx", "resp", None))
    return client


class TestExecutionPrice(unittest.IsolatedAsyncioTestCase):
    async def test_empty_side_has_no_price(self):
        client = client_with_book(asks=[], bids=[order("3000.00", "1.0")])
        price, matched = await client.get_potential_execution_price(0, 100, is_ask=False)
        self.assertIsNone(price)
        self.assertEqual(matched, 0)

    async def test_if_slippage_reports_empty_book(self):
        for is_ask in (True, False):
            client = client_with_book(asks=[], bids=[])
            _, _, err = await client.create_market_order_if_slippage(
                0, 1, 100, 0.01, is_ask, ideal_price=300000,
            )
            self.assertEqual(err, SIZE_ERROR)
            client.create_order.assert_not_called()

    async def test_quote_amount_reports_empty_book(self):
        for is_ask in (True, False):
            client = client_with_book(asks=[], bids=[])
            _, _, err = await client.create_market_order_quote_amount(
                0, 1, 10, 0.01, is_ask, ideal_price=300000,
            )
            self.assertEqual(err, SIZE_ERROR)
            client.create_order.assert_not_called()

    async def test_if_slippage_sends_order_within_slippage(self):
        client = client_with_book(asks=[order("3000.00", "1.0")], bids=[])
        _, _, err = await client.create_market_order_if_slippage(0, 1, 5, 0.01, False, ideal_price=300000)
        self.assertIsNone(err)
        self.assertEqual(client.create_order.call_args.kwargs["price"], 303000)


if __name__ == "__main__":
    unittest.main()
