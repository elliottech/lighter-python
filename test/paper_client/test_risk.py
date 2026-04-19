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

    def test_health_bankruptcy(self):
        a = new_paper_account(1)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 200.0, 0)
        health = compute_health(a, {0: 100.0}, {0: cfg()})
        self.assertEqual(health.status, PaperHealthStatus.BANKRUPTCY)

    def test_margin_usage_inf_when_underwater_with_position(self):
        a = new_paper_account(1)
        apply_fill(a, 0, PaperOrderSide.BUY, 1.0, 200.0, 0)
        # TAV = 1 + (100 - 200) = -99 <= 0, position still open so IMR > 0
        health = compute_health(a, {0: 100.0}, {0: cfg()})
        self.assertEqual(health.margin_usage, float("inf"))
        self.assertAlmostEqual(health.leverage, 0.0)

    def test_margin_usage_zero_when_no_positions(self):
        # Flat account with no IMR should read 0.0, not inf.
        a = new_paper_account(1000)
        health = compute_health(a, {}, {})
        self.assertEqual(health.status, PaperHealthStatus.HEALTHY)
        self.assertAlmostEqual(health.margin_usage, 0.0)

        # Same rule after a round-trip wipes collateral to zero / negative.
        a2 = new_paper_account(1)
        apply_fill(a2, 0, PaperOrderSide.BUY, 1.0, 200.0, 10)
        apply_fill(a2, 0, PaperOrderSide.SELL, 1.0, 100.0, 10)
        # No positions remaining, TAV <= 0 due to realized loss + fees.
        health2 = compute_health(a2, {0: 100.0}, {0: cfg()})
        self.assertAlmostEqual(health2.margin_usage, 0.0)


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

    def test_liquidation_scenario(self):
        # User longs 0.05 BTC at $100k with $1000 collateral, 10% IMF / 5% MMF.
        # Mark drifts down through pre-liquidation and crosses liq_price;
        # position gets wiped, and has_been_liquidated gets flagged on get_health().
        a = new_paper_account(1000)
        c = {0: cfg(0, imf=1000, mmf=500, comf=250)}
        apply_fill(a, 0, PaperOrderSide.BUY, 0.05, 100_000.0, 0)

        # T0 - just opened, healthy
        h0 = compute_health(a, {0: 100_000.0}, c)
        self.assertEqual(h0.status, PaperHealthStatus.HEALTHY)
        self.assertFalse(h0.has_been_liquidated)
        self.assertAlmostEqual(h0.total_account_value, 1000.0)
        self.assertAlmostEqual(h0.margin_usage, 50.0)

        # T1 - mark drops to 92k, still healthy
        h1 = compute_health(a, {0: 92_000.0}, c)
        self.assertEqual(h1.status, PaperHealthStatus.HEALTHY)
        self.assertFalse(h1.has_been_liquidated)

        # T2 - mark drops to 88k, enters pre-liquidation
        h2 = compute_health(a, {0: 88_000.0}, c)
        self.assertEqual(h2.status, PaperHealthStatus.PRE_LIQUIDATION)
        self.assertFalse(h2.has_been_liquidated)
        self.assertGreater(h2.margin_usage, 100.0)

        # T3 - mark crosses liq_price, liquidation fires
        liquidated = check_and_liquidate(a, {0: 84_000.0}, c)
        self.assertEqual(liquidated, [0])
        self.assertNotIn(0, a.positions)
        self.assertTrue(a.trades[-1].is_liquidation)

        # T4 continued - health now reads HEALTHY (no positions) BUT the
        # sticky flag tells the user what happened.
        h3 = compute_health(a, {0: 84_000.0}, c)
        self.assertEqual(h3.status, PaperHealthStatus.HEALTHY)
        self.assertTrue(h3.has_been_liquidated)
        self.assertEqual(h3.initial_margin_requirement, 0.0)
        self.assertEqual(h3.maintenance_margin_requirement, 0.0)
        self.assertAlmostEqual(h3.margin_usage, 0.0)  
        self.assertLess(h3.total_account_value, 1000.0)


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
