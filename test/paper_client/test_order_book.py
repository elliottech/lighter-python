import unittest

from lighter.models.order_book_depth import OrderBookDepth
from lighter.models.order_book_orders import OrderBookOrders
from lighter.models.price_level import PriceLevel
from lighter.models.simple_order import SimpleOrder
from lighter.paper_client.order_book import InMemoryOrderBook


def make_runtime() -> InMemoryOrderBook:
    return InMemoryOrderBook(
        asks=[
            {"price": "3000.00", "size": "1.0"},
            {"price": "3001.00", "size": "2.0"},
        ],
        bids=[
            {"price": "2999.00", "size": "1.5"},
            {"price": "2998.00", "size": "2.5"},
        ],
    )


class TestOrderBookRuntime(unittest.TestCase):
    def test_apply_snapshot_normalizes_rest_orders_and_sorts(self) -> None:
        book = InMemoryOrderBook()

        snapshot = OrderBookOrders(
            code=0,
            total_asks=2,
            asks=[
                SimpleOrder(
                    order_index=1,
                    order_id="ask-2",
                    owner_account_index=10,
                    initial_base_amount="1.0",
                    remaining_base_amount="2.0",
                    price="3001.00",
                    order_expiry=0,
                    transaction_time=0,
                ),
                SimpleOrder(
                    order_index=2,
                    order_id="ask-1",
                    owner_account_index=10,
                    initial_base_amount="1.0",
                    remaining_base_amount="1.0",
                    price="3000.00",
                    order_expiry=0,
                    transaction_time=0,
                ),
            ],
            total_bids=2,
            bids=[
                SimpleOrder(
                    order_index=3,
                    order_id="bid-1",
                    owner_account_index=10,
                    initial_base_amount="1.0",
                    remaining_base_amount="1.5",
                    price="2999.00",
                    order_expiry=0,
                    transaction_time=0,
                ),
                SimpleOrder(
                    order_index=4,
                    order_id="bid-2",
                    owner_account_index=10,
                    initial_base_amount="1.0",
                    remaining_base_amount="1.0",
                    price="2998.00",
                    order_expiry=0,
                    transaction_time=0,
                ),
            ],
        )

        book.apply_snapshot(snapshot)

        self.assertEqual([level.price for level in book.asks], ["3000.00", "3001.00"])
        self.assertEqual([level.size for level in book.asks], ["1.0", "2.0"])
        self.assertEqual([level.price for level in book.bids], ["2999.00", "2998.00"])
        self.assertIsNone(book.offset)
        self.assertIsNotNone(book.best_ask)
        self.assertIsNotNone(book.best_bid)
        self.assertEqual(book.best_ask.price, "3000.00")
        self.assertEqual(book.best_bid.price, "2999.00")
        self.assertEqual(book.mid_price, 2999.5)

    def test_apply_delta_removes_existing_level_for_zero_string(self) -> None:
        book = make_runtime()

        book.apply_delta({"asks": [{"price": "3000.00", "size": "0"}], "bids": []})

        self.assertEqual([level.price for level in book.asks], ["3001.00"])

    def test_apply_delta_removes_existing_level_for_zero_point_zero(self) -> None:
        book = make_runtime()

        book.apply_delta({"asks": [{"price": "3000.00", "size": "0.0"}], "bids": []})

        self.assertEqual([level.price for level in book.asks], ["3001.00"])

    def test_apply_delta_removes_existing_level_for_zero_point_zero_zero_zero(
        self,
    ) -> None:
        book = make_runtime()

        book.apply_delta({"asks": [{"price": "3000.00", "size": "0.0000"}], "bids": []})

        self.assertEqual([level.price for level in book.asks], ["3001.00"])

    def test_apply_delta_ignores_tombstone_for_missing_level(self) -> None:
        book = make_runtime()

        book.apply_delta({"asks": [{"price": "9999.00", "size": "0.0000"}], "bids": []})

        self.assertEqual([level.price for level in book.asks], ["3000.00", "3001.00"])

    def test_apply_delta_replaces_existing_size_for_non_zero_update(self) -> None:
        book = make_runtime()

        book.apply_delta({"asks": [{"price": "3000.00", "size": "2.5"}], "bids": []})

        self.assertEqual(len(book.asks), 2)
        self.assertEqual(book.asks[0].price, "3000.00")
        self.assertEqual(book.asks[0].size, "2.5")

    def test_apply_delta_accepts_order_book_depth_and_price_levels(self) -> None:
        book = make_runtime()

        book.apply_delta(
            OrderBookDepth(
                code=0,
                asks=[
                    PriceLevel(price="3001.00", size="0.0000"),
                    PriceLevel(price="2999.50", size="0.7"),
                ],
                bids=[
                    PriceLevel(price="2999.00", size="2.25"),
                    PriceLevel(price="3000.00", size="0.4"),
                ],
                offset=43,
                nonce=7,
            )
        )

        self.assertEqual(
            [level.to_dict() for level in book.asks],
            [
                {"price": "2999.50", "size": "0.7"},
                {"price": "3000.00", "size": "1.0"},
            ],
        )
        self.assertEqual(
            [level.to_dict() for level in book.bids],
            [
                {"price": "3000.00", "size": "0.4"},
                {"price": "2999.00", "size": "2.25"},
                {"price": "2998.00", "size": "2.5"},
            ],
        )
        self.assertEqual(book.offset, 43)

    def test_apply_delta_inserts_new_levels_and_keeps_final_book_sorted(self) -> None:
        book = make_runtime()

        book.apply_delta(
            {
                "asks": [
                    {"price": "2999.50", "size": "0.7"},
                    {"price": "3005.00", "size": "0.8"},
                ],
                "bids": [
                    {"price": "2999.50", "size": "0.6"},
                    {"price": "2997.50", "size": "0.4"},
                ],
                "offset": 42,
            }
        )

        self.assertEqual(
            [level.price for level in book.asks],
            ["2999.50", "3000.00", "3001.00", "3005.00"],
        )
        self.assertEqual(
            [level.price for level in book.bids],
            ["2999.50", "2999.00", "2998.00", "2997.50"],
        )
        self.assertEqual(book.offset, 42)

    def test_mid_price_is_none_when_either_side_is_missing(self) -> None:
        self.assertIsNone(InMemoryOrderBook().mid_price)
        self.assertIsNone(
            InMemoryOrderBook(asks=[{"price": "3000.00", "size": "1.0"}]).mid_price
        )
        self.assertIsNone(
            InMemoryOrderBook(bids=[{"price": "2999.00", "size": "1.0"}]).mid_price
        )

    def test_snapshot_filters_zero_size_levels(self) -> None:
        book = InMemoryOrderBook()

        book.apply_snapshot(
            {
                "asks": [
                    {"price": "3000.00", "size": "0"},
                    {"price": "3001.00", "size": "1.25"},
                ],
                "bids": [
                    {"price": "2999.00", "size": "0.0000"},
                    {"price": "2998.00", "size": "2.5"},
                ],
                "offset": 11,
            }
        )

        self.assertEqual(
            [level.to_dict() for level in book.asks],
            [{"price": "3001.00", "size": "1.25"}],
        )
        self.assertEqual(
            [level.to_dict() for level in book.bids],
            [{"price": "2998.00", "size": "2.5"}],
        )
        self.assertEqual(book.offset, 11)

    def test_to_dict_returns_public_book_shape(self) -> None:
        book = make_runtime()
        book.apply_delta({"asks": [], "bids": [], "offset": 77})

        self.assertEqual(
            book.to_dict(),
            {
                "asks": [
                    {"price": "3000.00", "size": "1.0"},
                    {"price": "3001.00", "size": "2.0"},
                ],
                "bids": [
                    {"price": "2999.00", "size": "1.5"},
                    {"price": "2998.00", "size": "2.5"},
                ],
                "offset": 77,
            },
        )

    def test_invalid_level_payload_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "price and size"):
            InMemoryOrderBook(asks=[{"size": "1.0"}])

        with self.assertRaisesRegex(ValueError, "price and size"):
            InMemoryOrderBook(bids=[{"price": "2999.00"}])

    def test_asks_stay_ascending_after_mixed_updates(self) -> None:
        book = InMemoryOrderBook(
            asks=[
                {"price": "2111.04", "size": "304.1013"},
                {"price": "2111.36", "size": "474.9197"},
                {"price": "6666.00", "size": "1.8000"},
            ],
            bids=[],
        )

        book.apply_delta(
            {
                "asks": [
                    {"price": "6666.01", "size": "0.3000"},
                    {"price": "4050.00", "size": "0.3000"},
                ],
                "bids": [],
            }
        )

        self.assertEqual(
            [level.price for level in book.asks],
            ["2111.04", "2111.36", "4050.00", "6666.00", "6666.01"],
        )

    def test_bids_stay_descending_after_mixed_updates(self) -> None:
        book = InMemoryOrderBook(
            asks=[],
            bids=[
                {"price": "2103.36", "size": "451.4887"},
                {"price": "2102.72", "size": "474.9231"},
            ],
        )

        book.apply_delta(
            {
                "asks": [],
                "bids": [
                    {"price": "1893.31", "size": "0.0053"},
                    {"price": "2103.00", "size": "0.0100"},
                ],
            }
        )

        self.assertEqual(
            [level.price for level in book.bids],
            ["2103.36", "2103.00", "2102.72", "1893.31"],
        )


if __name__ == "__main__":
    unittest.main()
