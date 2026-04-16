import unittest

from lighter.paper_client.accounting import apply_fill, new_paper_account
from lighter.paper_client.risk import (
    check_and_liquidate,
    compute_closeout_margin_requirement,
    compute_health,
    compute_initial_margin_requirement,
    compute_liquidation_price,
    compute_maintenance_margin_requirement,
    update_position_metrics,
)
from lighter.paper_client.types import PaperHealthStatus, PaperOrderSide
from test.paper_client.helpers import cfg


class TestMarginRequirements(unittest.TestCase):
    def test_margin_requirements(self):
        a = new_paper_account(1000)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
        c = {0: cfg(0, imf=1000, mmf=500, comf=250)}
        mp = {0: 100.0}
        self.assertAlmostEqual(compute_initial_margin_requirement(a, mp, c), 10.0)
        self.assertAlmostEqual(compute_maintenance_margin_requirement(a, mp, c), 5.0)
        self.assertAlmostEqual(compute_closeout_margin_requirement(a, mp, c), 2.5)


class TestHealth(unittest.TestCase):
    def test_health_healthy(self):
        a = new_paper_account(1000)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
        health = compute_health(a, {0: 100.0}, {0: cfg()})
        self.assertEqual(health.status, PaperHealthStatus.HEALTHY)

    def test_health_pre_liquidation(self):
        a = new_paper_account(9)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
        health = compute_health(a, {0: 100.0}, {0: cfg()})
        self.assertEqual(health.status, PaperHealthStatus.PRE_LIQUIDATION)

    def test_health_partial_liquidation(self):
        a = new_paper_account(4.5)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
        health = compute_health(a, {0: 100.0}, {0: cfg()})
        self.assertEqual(health.status, PaperHealthStatus.PARTIAL_LIQUIDATION)

    def test_health_full_liquidation(self):
        a = new_paper_account(2)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
        health = compute_health(a, {0: 100.0}, {0: cfg()})
        self.assertEqual(health.status, PaperHealthStatus.FULL_LIQUIDATION)

    def test_health_bankruptcy(self):
        a = new_paper_account(1)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 200.0, 0)
        health = compute_health(a, {0: 100.0}, {0: cfg()})
        self.assertEqual(health.status, PaperHealthStatus.BANKRUPTCY)

    def test_margin_usage_and_leverage_zero_tav(self):
        a = new_paper_account(1)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 200.0, 0)
        # TAV = 1 + (100 - 200) = -99 <= 0
        health = compute_health(a, {0: 100.0}, {0: cfg()})
        self.assertAlmostEqual(health.margin_usage, 0.0)
        self.assertAlmostEqual(health.leverage, 0.0)


class TestLiquidationPrice(unittest.TestCase):
    def test_liquidation_price_long(self):
        a = new_paper_account(15)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
        lp = compute_liquidation_price(a, 0, {0: 100.0}, {0: cfg()})
        self.assertGreater(lp, 0.0)
        self.assertLess(lp, 100.0)

    def test_liquidation_price_short(self):
        a = new_paper_account(100)
        apply_fill(a, 0, PaperOrderSide.SELL, 1.0, 100.0, 0)
        lp = compute_liquidation_price(a, 0, {0: 100.0}, {0: cfg()})
        self.assertGreater(lp, 100.0)

    def test_liquidation_price_clamped_negative(self):
        a = new_paper_account(10_000_000)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
        lp = compute_liquidation_price(a, 0, {0: 100.0}, {0: cfg()})
        self.assertAlmostEqual(lp, 0.0)

    def test_liquidation_price_capped_at_mark(self):
        a = new_paper_account(2)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
        lp = compute_liquidation_price(a, 0, {0: 100.0}, {0: cfg()})
        self.assertAlmostEqual(lp, 100.0)

    def test_liquidation_price_no_position(self):
        a = new_paper_account(1000)
        lp = compute_liquidation_price(a, 99, {99: 100.0}, {99: cfg(99)})
        self.assertAlmostEqual(lp, 0.0)


class TestCheckAndLiquidate(unittest.TestCase):
    def test_check_and_liquidate_short(self):
        a = new_paper_account(5)
        apply_fill(a, 0, PaperOrderSide.SELL, 1.0, 100.0, 0)
        liquidated = check_and_liquidate(a, {0: 200.0}, {0: cfg()})
        self.assertIn(0, liquidated)
        self.assertNotIn(0, a.positions)
        liq_trade = a.trades[-1]
        self.assertTrue(liq_trade.is_liquidation)


class TestUpdatePositionMetrics(unittest.TestCase):
    def test_update_position_metrics(self):
        a = new_paper_account(20)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
        update_position_metrics(a, {0: 120.0}, {0: cfg()})
        pos = a.positions[0]
        self.assertAlmostEqual(pos.mark_price, 120.0)
        self.assertAlmostEqual(pos.unrealized_pnl, 20.0)
        self.assertGreater(pos.liquidation_price, 0.0)


if __name__ == "__main__":
    unittest.main()
