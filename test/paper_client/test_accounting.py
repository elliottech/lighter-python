import unittest

from lighter.paper_client.accounting import (
    apply_fill,
    compute_unrealized_pnl,
    compute_total_account_value,
    new_paper_account,
)
from lighter.paper_client.types import PaperOrderSide, PaperPosition


class TestApplyFill(unittest.TestCase):
    def test_open_new_long(self):
        a = new_paper_account(10000.0)
        apply_fill(a, market_id=0, side=PaperOrderSide.BUY, fill_size=1.0, fill_price=100.0, fee=0.5)
        pos = a.positions[0]
        self.assertAlmostEqual(pos.size, 1.0)
        self.assertAlmostEqual(pos.entry_quote, 100.0)
        self.assertAlmostEqual(a.collateral, 10000.0 - 0.5)

    def test_open_new_short(self):
        a = new_paper_account(10000.0)
        apply_fill(a, market_id=0, side=PaperOrderSide.SELL, fill_size=1.0, fill_price=100.0, fee=0.5)
        pos = a.positions[0]
        self.assertAlmostEqual(pos.size, -1.0)
        self.assertAlmostEqual(pos.entry_quote, 100.0)
        self.assertAlmostEqual(a.collateral, 10000.0 - 0.5)

    def test_increase_existing_long(self):
        a = new_paper_account(10000.0)
        apply_fill(a, market_id=0, side=PaperOrderSide.BUY, fill_size=1.0, fill_price=100.0, fee=0.0)
        apply_fill(a, market_id=0, side=PaperOrderSide.BUY, fill_size=1.0, fill_price=110.0, fee=0.0)
        pos = a.positions[0]
        self.assertAlmostEqual(pos.size, 2.0)
        self.assertAlmostEqual(pos.entry_quote, 210.0)

    def test_partial_close_long(self):
        a = new_paper_account(10000.0)
        apply_fill(a, market_id=0, side=PaperOrderSide.BUY, fill_size=2.0, fill_price=100.0, fee=0.0)
        pnl = apply_fill(a, market_id=0, side=PaperOrderSide.SELL, fill_size=1.0, fill_price=120.0, fee=0.0)
        pos = a.positions[0]
        self.assertAlmostEqual(pnl, 20.0)
        self.assertAlmostEqual(pos.entry_quote, 100.0)
        self.assertAlmostEqual(a.collateral, 10000.0 + 20.0)

    def test_partial_close_short(self):
        a = new_paper_account(10000.0)
        apply_fill(a, market_id=0, side=PaperOrderSide.SELL, fill_size=2.0, fill_price=100.0, fee=0.0)
        pnl = apply_fill(a, market_id=0, side=PaperOrderSide.BUY, fill_size=1.0, fill_price=80.0, fee=0.0)
        self.assertAlmostEqual(pnl, 20.0)

    def test_flip_long_to_short(self):
        a = new_paper_account(10000.0)
        apply_fill(a, market_id=0, side=PaperOrderSide.BUY, fill_size=1.0, fill_price=100.0, fee=0.0)
        pnl = apply_fill(a, market_id=0, side=PaperOrderSide.SELL, fill_size=3.0, fill_price=120.0, fee=0.0)
        pos = a.positions[0]
        self.assertAlmostEqual(pnl, 20.0)
        self.assertAlmostEqual(pos.size, -2.0)
        self.assertAlmostEqual(pos.entry_quote, 240.0)

    def test_full_close_removes_position(self):
        a = new_paper_account(10000.0)
        apply_fill(a, market_id=0, side=PaperOrderSide.BUY, fill_size=1.0, fill_price=100.0, fee=0.0)
        pnl = apply_fill(a, market_id=0, side=PaperOrderSide.SELL, fill_size=1.0, fill_price=110.0, fee=0.0)
        self.assertNotIn(0, a.positions)
        self.assertAlmostEqual(pnl, 10.0)


class TestUnrealizedPnl(unittest.TestCase):
    def test_unrealized_pnl_long(self):
        pos = PaperPosition(market_id=0, size=1.0, entry_quote=100.0)
        self.assertAlmostEqual(compute_unrealized_pnl(pos, mark_price=120.0), 20.0)
        self.assertAlmostEqual(compute_unrealized_pnl(pos, mark_price=80.0), -20.0)

    def test_unrealized_pnl_short(self):
        pos = PaperPosition(market_id=0, size=-1.0, entry_quote=100.0)
        self.assertAlmostEqual(compute_unrealized_pnl(pos, mark_price=80.0), 20.0)
        self.assertAlmostEqual(compute_unrealized_pnl(pos, mark_price=120.0), -20.0)


class TestTotalAccountValue(unittest.TestCase):
    def test_total_account_value(self):
        a = new_paper_account(1000.0)
        # long 1@100 on market 0
        apply_fill(a, market_id=0, side=PaperOrderSide.BUY, fill_size=1.0, fill_price=100.0, fee=0.0)
        # short 1@200 on market 1
        apply_fill(a, market_id=1, side=PaperOrderSide.SELL, fill_size=1.0, fill_price=200.0, fee=0.0)
        tav = compute_total_account_value(a, mark_prices={0: 110.0, 1: 190.0})
        self.assertAlmostEqual(tav, 1020.0)


if __name__ == "__main__":
    unittest.main()
