import asyncio
import json
import unittest
from typing import Any, Dict, List, Optional

import websockets

from lighter.paper_client.accounting import apply_fill
from lighter.paper_client import (
    PaperClient,
    PaperHealthStatus,
    PaperOrderRequest,
    PaperOrderSide,
)
from test.paper_client.helpers import FakeOrderApi, default_detail


def subscribed_message(market_id: int, asks, bids, offset: int) -> Dict[str, Any]:
    return {
        "type": "subscribed/order_book",
        "channel": f"order_book:{market_id}",
        "order_book": {
            "asks": [{"price": p, "size": s} for p, s in asks],
            "bids": [{"price": p, "size": s} for p, s in bids],
            "offset": offset,
        },
    }


def update_message(market_id: int, asks, bids, offset: int) -> Dict[str, Any]:
    return {
        "type": "update/order_book",
        "channel": f"order_book/{market_id}",
        "order_book": {
            "asks": [{"price": p, "size": s} for p, s in asks],
            "bids": [{"price": p, "size": s} for p, s in bids],
            "offset": offset,
        },
    }


async def wait_until(predicate, timeout: float = 2.0) -> None:
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while loop.time() < deadline:
        if predicate():
            return
        await asyncio.sleep(0.01)
    raise AssertionError("condition was not satisfied before timeout")


class LocalOrderBookWebSocket:
    def __init__(self, snapshot: Dict[str, Any]) -> None:
        self.snapshot = snapshot
        self.messages: asyncio.Queue = asyncio.Queue()
        self.received: List[Dict[str, Any]] = []
        self.closed = asyncio.Event()
        self.server = None
        self.url: Optional[str] = None

    async def __aenter__(self):
        self.server = await websockets.serve(self._handler, "127.0.0.1", 0)
        port = self.server.sockets[0].getsockname()[1]
        self.url = f"ws://127.0.0.1:{port}"
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.messages.put(None)
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()

    async def push(self, message: Dict[str, Any]) -> None:
        await self.messages.put(message)

    async def _handler(self, websocket, *args) -> None:
        try:
            await websocket.send(json.dumps({"type": "connected"}))
            while True:
                raw_message = await websocket.recv()
                message = json.loads(raw_message)
                self.received.append(message)
                if message.get("type") == "subscribe":
                    await websocket.send(json.dumps(self.snapshot))
                    break

            while True:
                next_outbound = asyncio.create_task(self.messages.get())
                next_inbound = asyncio.create_task(websocket.recv())
                done, pending = await asyncio.wait(
                    [next_outbound, next_inbound],
                    return_when=asyncio.FIRST_COMPLETED,
                )

                for task in pending:
                    task.cancel()

                if next_inbound in done:
                    try:
                        self.received.append(json.loads(next_inbound.result()))
                    except Exception:
                        break
                    continue

                outbound = next_outbound.result()
                if outbound is None:
                    break
                await websocket.send(json.dumps(outbound))
        finally:
            self.closed.set()


class MultiMarketWebSocket:
    """WS server that routes snapshots and updates per market across connections."""

    def __init__(self, snapshots: Dict[int, Dict[str, Any]]) -> None:
        self.snapshots = snapshots
        self._queues: Dict[int, asyncio.Queue] = {}
        self.closed_markets: set = set()
        self.server = None
        self.url: Optional[str] = None

    async def __aenter__(self):
        self.server = await websockets.serve(self._handler, "127.0.0.1", 0)
        port = self.server.sockets[0].getsockname()[1]
        self.url = f"ws://127.0.0.1:{port}"
        return self

    async def __aexit__(self, exc_type, exc, tb):
        for q in self._queues.values():
            await q.put(None)
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()

    async def push(self, market_id: int, message: Dict[str, Any]) -> None:
        q = self._queues.get(market_id)
        if q is not None:
            await q.put(message)

    async def _handler(self, websocket, *args) -> None:
        market_id = None
        q = asyncio.Queue()
        try:
            await websocket.send(json.dumps({"type": "connected"}))
            while True:
                raw = await websocket.recv()
                msg = json.loads(raw)
                if msg.get("type") == "subscribe":
                    channel = msg.get("channel", "")
                    market_id = int(channel.split("/")[-1])
                    self._queues[market_id] = q
                    await websocket.send(json.dumps(self.snapshots[market_id]))
                    break

            while True:
                next_out = asyncio.create_task(q.get())
                next_in = asyncio.create_task(websocket.recv())
                done, pending = await asyncio.wait(
                    [next_out, next_in],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                for t in pending:
                    t.cancel()
                if next_in in done:
                    try:
                        next_in.result()
                    except Exception:
                        break
                    continue
                out = next_out.result()
                if out is None:
                    break
                await websocket.send(json.dumps(out))
        finally:
            if market_id is not None:
                self.closed_markets.add(market_id)


class TestPaperClientLive(unittest.IsolatedAsyncioTestCase):
    async def test_track_market_subscribes_and_applies_snapshot(self) -> None:
        snapshot = subscribed_message(
            0,
            asks=[("3002.00", "2.0"), ("3000.00", "1.0")],
            bids=[("2998.00", "1.5"), ("2999.00", "1.0")],
            offset=11,
        )

        async with LocalOrderBookWebSocket(snapshot) as ws:
            client = PaperClient(
                None,
                5000.0,
                order_api=FakeOrderApi(),
                ws_url=ws.url,
            )

            await client.track_market(0)

            self.assertEqual(
                ws.received[0],
                {"type": "subscribe", "channel": "order_book/0"},
            )
            self.assertEqual(
                [level.to_dict() for level in client.order_books[0].asks],
                [
                    {"price": "3000.00", "size": "1.0"},
                    {"price": "3002.00", "size": "2.0"},
                ],
            )
            self.assertEqual(
                [level.price for level in client.order_books[0].bids],
                ["2999.00", "2998.00"],
            )
            self.assertEqual(client.order_books[0].offset, 11)

            await client.close()

    async def test_live_updates_tombstones_sorting_offset_and_cleanup(self) -> None:
        snapshot = subscribed_message(
            0,
            asks=[("3000.00", "1.0"), ("3002.00", "1.0")],
            bids=[("2999.00", "1.0"), ("2998.00", "1.0")],
            offset=11,
        )

        async with LocalOrderBookWebSocket(snapshot) as ws:
            client = PaperClient(
                None,
                5000.0,
                order_api=FakeOrderApi(),
                ws_url=ws.url,
            )
            await client.track_market(0)

            await ws.push(
                update_message(
                    0,
                    asks=[("3000.00", "0.0000"), ("2997.00", "0.5")],
                    bids=[("2998.00", "0.0"), ("3001.00", "0.25")],
                    offset=12,
                )
            )

            await wait_until(lambda: client.order_books[0].offset == 12)

            self.assertEqual(
                [level.to_dict() for level in client.order_books[0].asks],
                [
                    {"price": "2997.00", "size": "0.5"},
                    {"price": "3002.00", "size": "1.0"},
                ],
            )
            self.assertEqual(
                [level.to_dict() for level in client.order_books[0].bids],
                [
                    {"price": "3001.00", "size": "0.25"},
                    {"price": "2999.00", "size": "1.0"},
                ],
            )

            await client.stop_tracking(0)
            self.assertNotIn(0, client._live_listeners)
            await wait_until(lambda: ws.closed.is_set())

    async def test_live_update_liquidates_position(self) -> None:
        order_api = FakeOrderApi()
        order_api.details[0].maintenance_margin_fraction = 500
        order_api.details[0].closeout_margin_fraction = 250
        order_api.details[0].taker_fee = "0"
        snapshot = subscribed_message(
            0,
            asks=[("100.00", "10.0")],
            bids=[("99.00", "10.0")],
            offset=1,
        )

        async with LocalOrderBookWebSocket(snapshot) as ws:
            client = PaperClient(
                None,
                5.0,
                order_api=order_api,
                ws_url=ws.url,
            )
            await client.track_market(0)
            apply_fill(client.account, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)

            await ws.push(
                update_message(
                    0,
                    asks=[("100.00", "0"), ("10.00", "10.0")],
                    bids=[("99.00", "0.0000"), ("9.00", "10.0")],
                    offset=2,
                )
            )

            await wait_until(lambda: client.get_position(0) is None)
            self.assertTrue(client.get_trades()[-1].is_liquidation)

            await client.close()


    async def test_live_multi_market_trading_and_metrics(self) -> None:
        snapshots = {
            0: subscribed_message(0, [("3000.00", "5.0")], [("2999.00", "5.0")], 1),
            1: subscribed_message(1, [("60000.00", "1.0")], [("59999.00", "1.0")], 1),
        }

        async with MultiMarketWebSocket(snapshots) as ws:
            order_api = FakeOrderApi()
            order_api.details[1].last_trade_price = 60000.0
            order_api.details[1].min_base_amount = "0.0001"
            client = PaperClient(None, 10000.0, order_api=order_api, ws_url=ws.url)

            await client.track_market(0)
            await client.track_market(1)

            # Place orders against live book
            await client.create_paper_order(PaperOrderRequest(0, PaperOrderSide.BUY, 1.0))
            await client.create_paper_order(PaperOrderRequest(1, PaperOrderSide.BUY, 0.01))
            self.assertAlmostEqual(client.get_position(0).size, 1.0)
            self.assertAlmostEqual(client.get_position(1).size, 0.01)

            # Delta 1: ETH price moves up (tombstone old, add new)
            await ws.push(0, update_message(0,
                asks=[("3000.00", "0"), ("3100.00", "5.0")],
                bids=[("2999.00", "0"), ("3099.00", "5.0")],
                offset=2,
            ))
            await wait_until(lambda: client.order_books[0].offset == 2)

            pos0 = client.get_position(0)
            self.assertAlmostEqual(pos0.mark_price, 3099.5)
            self.assertAlmostEqual(pos0.unrealized_pnl, 99.5)

            # Delta 2: ETH price moves further
            await ws.push(0, update_message(0,
                asks=[("3100.00", "0"), ("3200.00", "5.0")],
                bids=[("3099.00", "0"), ("3199.00", "5.0")],
                offset=3,
            ))
            await wait_until(lambda: client.order_books[0].offset == 3)

            pos0 = client.get_position(0)
            self.assertAlmostEqual(pos0.mark_price, 3199.5)
            self.assertAlmostEqual(pos0.unrealized_pnl, 199.5)

            # Cross-margin health uses both positions
            health = client.get_health()
            self.assertEqual(health.status, PaperHealthStatus.HEALTHY)
            self.assertGreater(health.leverage, 0)

            # close() cleans up both listeners
            await client.close()
            self.assertEqual(len(client._live_listeners), 0)
            await wait_until(lambda: len(ws.closed_markets) == 2)

    async def test_live_liquidation_state_inspection(self) -> None:
        order_api = FakeOrderApi()
        order_api.details[0] = default_detail(0, "ETH", last_trade_price=100.0)
        order_api.details[0].maintenance_margin_fraction = 500
        order_api.details[0].closeout_margin_fraction = 250
        order_api.details[0].taker_fee = "0"
        order_api.details[1] = default_detail(1, "ALT", last_trade_price=10.0)
        order_api.details[1].taker_fee = "0"

        snapshots = {
            0: subscribed_message(0, [("100.00", "10.0")], [("99.00", "10.0")], 1),
            1: subscribed_message(1, [("10.00", "10.0")], [("9.99", "10.0")], 1),
        }

        async with MultiMarketWebSocket(snapshots) as ws:
            client = PaperClient(None, 20.0, order_api=order_api, ws_url=ws.url)

            await client.track_market(0)
            await client.track_market(1)

            apply_fill(client.account, 0, PaperOrderSide.BUY, 1.0, 100.0, 0)
            apply_fill(client.account, 1, PaperOrderSide.BUY, 1.0, 10.0, 0)
            collateral_before = client.get_collateral()

            # Crash market 0 → TAV drops below cross_MMR → cascade liquidation
            await ws.push(0, update_message(0,
                asks=[("100.00", "0"), ("84.00", "10.0")],
                bids=[("99.00", "0"), ("82.00", "10.0")],
                offset=2,
            ))
            await wait_until(lambda: client.get_position(0) is None)

            # Cross-margin cascade: both positions liquidated
            self.assertIsNone(client.get_position(0))
            self.assertIsNone(client.get_position(1))

            # Collateral decreased by realized losses
            self.assertLess(client.get_collateral(), collateral_before)

            # Two liquidation trades with correct details
            liq_trades = [t for t in client.get_trades() if t.is_liquidation]
            self.assertEqual(len(liq_trades), 2)
            self.assertEqual({t.market_id for t in liq_trades}, {0, 1})
            mkt0_liq = next(t for t in liq_trades if t.market_id == 0)
            self.assertLess(mkt0_liq.realized_pnl, -10)

            # No positions left → healthy with remaining collateral
            health = client.get_health()
            self.assertGreater(health.total_account_value, 0)
            self.assertAlmostEqual(health.leverage, 0.0)

            await client.close()


if __name__ == "__main__":
    unittest.main()
