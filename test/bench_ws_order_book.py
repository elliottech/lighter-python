"""Benchmark WsClient order book updates: indexed sorted levels vs. the previous list scan.

Run: python test/bench_ws_order_book.py
Not collected by pytest (file name does not start with test_).
"""
import random
import statistics
import time

from lighter.ws_client import WsClient


def make_stream(levels, n_updates, seed=0):
    rng = random.Random(seed)
    mid = 100_000.0
    asks = [{"price": f"{mid + 0.1 * (i + 1):.1f}", "size": "1.00000"} for i in range(levels)]
    bids = [{"price": f"{mid - 0.1 * (i + 1):.1f}", "size": "1.00000"} for i in range(levels)]
    width = levels * 1.2
    stream = []
    for _ in range(n_updates):
        upd = {"asks": [], "bids": []}
        for _ in range(rng.randint(1, 8)):
            side = rng.choice(["asks", "bids"])
            off = 0.1 * rng.randint(1, int(width))
            price = mid + off if side == "asks" else mid - off
            size = "0.00000" if rng.random() < 0.3 else f"{rng.uniform(0.001, 5):.5f}"
            upd[side].append({"price": f"{price:.1f}", "size": size})
        stream.append(upd)
    return asks, bids, stream


def run_new(asks, bids, stream):
    client = WsClient(ws_url="wss://example.invalid/stream", order_book_ids=[1],
                      on_order_book_update=None, verify_order_book_continuity=False)
    client.handle_subscribed_order_book({"channel": "order_book:1", "order_book": {
        "asks": [dict(o) for o in asks], "bids": [dict(o) for o in bids]}})
    t = time.perf_counter()
    for upd in stream:
        client.update_order_book_state("1", {"asks": [dict(o) for o in upd["asks"]],
                                             "bids": [dict(o) for o in upd["bids"]]})
    return time.perf_counter() - t


def run_old(asks, bids, stream):
    client = WsClient(ws_url="wss://example.invalid/stream", order_book_ids=[1], on_order_book_update=None)
    state = {"asks": [dict(o) for o in asks], "bids": [dict(o) for o in bids]}
    t = time.perf_counter()
    for upd in stream:
        # the previous update_order_book_state body
        client.update_orders([dict(o) for o in upd["asks"]], state["asks"])
        client.update_orders([dict(o) for o in upd["bids"]], state["bids"])
    return time.perf_counter() - t


if __name__ == "__main__":
    print(f"{'levels/side':>11} {'updates':>8} {'old median s':>13} {'new median s':>13} {'speedup':>8}")
    for levels in (50, 200, 1000):
        n = 3_000
        asks, bids, stream = make_stream(levels, n)
        old = statistics.median(run_old(asks, bids, stream) for _ in range(5))
        new = statistics.median(run_new(asks, bids, stream) for _ in range(5))
        print(f"{levels:>11} {n:>8} {old:>13.4f} {new:>13.4f} {old / new:>7.1f}x")
