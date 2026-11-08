import asyncio
import json
import random
from decimal import Decimal

from lighter.ws_client import WsClient


class FakeWs:
    def __init__(self):
        self.sent = []

    def send(self, payload):
        self.sent.append(json.loads(payload))


class FakeAsyncWs:
    def __init__(self):
        self.sent = []

    async def send(self, payload):
        self.sent.append(json.loads(payload))


def make_client(**kwargs):
    kwargs.setdefault("on_order_book_update", None)
    return WsClient(ws_url="wss://example.invalid/stream", order_book_ids=[1], **kwargs)


def snapshot(asks, bids, nonce=100, offset=10):
    return {
        "type": "subscribed/order_book",
        "channel": "order_book:1",
        "offset": offset,
        "order_book": {
            "code": 0,
            "asks": [{"price": p, "size": s} for p, s in asks],
            "bids": [{"price": p, "size": s} for p, s in bids],
            "offset": offset,
            "nonce": nonce,
            "begin_nonce": 0,
            "last_updated_at": 1,
        },
    }


def update(asks, bids, begin_nonce, nonce, offset=11):
    return {
        "type": "update/order_book",
        "channel": "order_book:1",
        "offset": offset,
        "order_book": {
            "code": 0,
            "asks": [{"price": p, "size": s} for p, s in asks],
            "bids": [{"price": p, "size": s} for p, s in bids],
            "offset": offset,
            "nonce": nonce,
            "begin_nonce": begin_nonce,
            "last_updated_at": 2,
        },
    }


def levels(side):
    return [(o["price"], o["size"]) for o in side]


def test_snapshot_is_sorted_and_zero_levels_dropped():
    client = make_client()
    client.on_message(FakeWs(), snapshot(
        asks=[("101.0", "1"), ("100.5", "2"), ("102.0", "0")],
        bids=[("99.0", "1"), ("99.5", "3"), ("98.0", "0.000")],
    ))
    book = client.order_book_states["1"]
    assert levels(book["asks"]) == [("100.5", "2"), ("101.0", "1")]
    assert levels(book["bids"]) == [("99.5", "3"), ("99.0", "1")]


def test_new_levels_inside_the_book_keep_best_prices_first():
    client = make_client()
    ws = FakeWs()
    client.on_message(ws, snapshot(asks=[("100.0", "1"), ("102.0", "1")], bids=[("98.0", "1"), ("96.0", "1")]))
    # Before this change these levels were appended at the end of the lists.
    client.on_message(ws, update(asks=[("101.0", "5"), ("99.5", "2")], bids=[("97.0", "4"), ("99.0", "3")],
                                 begin_nonce=100, nonce=105))
    book = client.order_book_states["1"]
    assert levels(book["asks"]) == [("99.5", "2"), ("100.0", "1"), ("101.0", "5"), ("102.0", "1")]
    assert levels(book["bids"]) == [("99.0", "3"), ("98.0", "1"), ("97.0", "4"), ("96.0", "1")]
    assert book["asks"][0]["price"] == "99.5" and book["bids"][0]["price"] == "99.0"


def test_size_changes_and_removals():
    client = make_client()
    ws = FakeWs()
    client.on_message(ws, snapshot(asks=[("100.0", "1"), ("101.0", "1")], bids=[("99.0", "1")]))
    client.on_message(ws, update(asks=[("100.0", "0.00000"), ("101.0", "7"), ("105.0", "0")],
                                 bids=[("99.00", "2")], begin_nonce=100, nonce=101))
    book = client.order_book_states["1"]
    assert levels(book["asks"]) == [("101.0", "7")]
    # "99.00" and "99.0" are the same price level
    assert levels(book["bids"]) == [("99.0", "2")]


def test_book_metadata_tracks_the_latest_update():
    client = make_client()
    ws = FakeWs()
    client.on_message(ws, snapshot(asks=[], bids=[], nonce=100, offset=10))
    client.on_message(ws, update(asks=[("1", "1")], bids=[], begin_nonce=100, nonce=103, offset=14))
    book = client.order_book_states["1"]
    assert (book["nonce"], book["begin_nonce"], book["offset"], book["last_updated_at"]) == (103, 100, 14, 2)


def test_gap_resubscribes_and_drops_deltas_until_fresh_snapshot():
    gaps = []
    updates = []
    client = make_client(on_order_book_gap=lambda m, e, g: gaps.append((m, e, g)),
                         on_order_book_update=lambda m, ob: updates.append(m))
    ws = FakeWs()
    client.on_message(ws, snapshot(asks=[("100.0", "1")], bids=[("99.0", "1")], nonce=100))
    client.on_message(ws, update(asks=[("100.0", "2")], bids=[], begin_nonce=100, nonce=110))
    # nonces 110..120 were missed
    client.on_message(ws, update(asks=[("100.0", "9")], bids=[], begin_nonce=120, nonce=125))
    assert gaps == [("1", 110, 120)]
    assert ws.sent == [{"type": "unsubscribe", "channel": "order_book/1"},
                       {"type": "subscribe", "channel": "order_book/1"}]
    assert levels(client.order_book_states["1"]["asks"]) == [("100.0", "2")]
    # deltas that arrive before the new snapshot are ignored, without another resubscribe
    client.on_message(ws, update(asks=[("100.0", "3")], bids=[], begin_nonce=125, nonce=126))
    assert len(ws.sent) == 2 and len(gaps) == 1
    client.on_message(ws, snapshot(asks=[("100.5", "4")], bids=[("99.0", "1")], nonce=130))
    client.on_message(ws, update(asks=[("100.5", "5")], bids=[], begin_nonce=130, nonce=131))
    assert levels(client.order_book_states["1"]["asks"]) == [("100.5", "5")]
    assert updates == ["1", "1", "1", "1"]  # snapshot, update, snapshot, update


def test_resync_unsubscribe_ack_is_not_reported_as_unhandled():
    unhandled = []
    client = make_client(on_unhandled_message=unhandled.append)
    ws = FakeWs()
    client.on_message(ws, snapshot(asks=[("100.0", "1")], bids=[], nonce=100))
    client.on_message(ws, update(asks=[], bids=[], begin_nonce=150, nonce=151))
    # shape observed from the testnet server after an unsubscribe
    client.on_message(ws, {"type": "unsubscribed", "channel": "order_book:1"})
    assert unhandled == []
    client.on_message(ws, snapshot(asks=[("100.0", "1")], bids=[], nonce=160))
    client.on_message(ws, {"type": "unsubscribed", "channel": "order_book:1"})
    assert unhandled == [{"type": "unsubscribed", "channel": "order_book:1"}]


def test_continuity_check_can_be_disabled():
    client = make_client(verify_order_book_continuity=False)
    ws = FakeWs()
    client.on_message(ws, snapshot(asks=[("100.0", "1")], bids=[], nonce=100))
    client.on_message(ws, update(asks=[("100.0", "2")], bids=[], begin_nonce=999, nonce=1000))
    assert levels(client.order_book_states["1"]["asks"]) == [("100.0", "2")]
    assert ws.sent == []


def test_async_path_awaits_resubscribe():
    client = make_client()
    ws = FakeAsyncWs()

    async def run():
        await client.on_message_async(ws, json.dumps(snapshot(asks=[("1", "1")], bids=[], nonce=5)))
        await client.on_message_async(ws, json.dumps(update(asks=[("1", "2")], bids=[], begin_nonce=7, nonce=8)))

    asyncio.run(run())
    assert ws.sent == [{"type": "unsubscribe", "channel": "order_book/1"},
                       {"type": "subscribe", "channel": "order_book/1"}]


def test_state_set_by_caller_is_indexed_on_first_update():
    client = make_client()
    client.order_book_states["1"] = {"asks": [{"price": "3", "size": "1"}, {"price": "1", "size": "1"}],
                                     "bids": [], "nonce": 1}
    client.update_order_book_state("1", {"asks": [{"price": "2", "size": "1"}], "bids": []})
    assert [o["price"] for o in client.order_book_states["1"]["asks"]] == ["1", "2", "3"]


def test_matches_reference_book_over_random_updates():
    rng = random.Random(0)
    client = make_client()
    ws = FakeWs()
    prices = [f"{100 + i * 0.5:.1f}" for i in range(200)]
    ref = {"asks": {}, "bids": {}}
    client.on_message(ws, snapshot(asks=[], bids=[], nonce=0))
    nonce = 0
    for _ in range(3000):
        asks, bids = [], []
        for _ in range(rng.randint(1, 6)):
            side = rng.choice(["asks", "bids"])
            price = rng.choice(prices)
            size = "0" if rng.random() < 0.3 else str(rng.randint(1, 50))
            (asks if side == "asks" else bids).append((price, size))
        client.on_message(ws, update(asks=asks, bids=bids, begin_nonce=nonce, nonce=nonce + 1))
        nonce += 1
        for side, rows in (("asks", asks), ("bids", bids)):
            for price, size in rows:
                if Decimal(size) == 0:
                    ref[side].pop(Decimal(price), None)
                else:
                    ref[side][Decimal(price)] = size
    book = client.order_book_states["1"]
    assert [(Decimal(p), s) for p, s in levels(book["asks"])] == sorted(ref["asks"].items())
    assert [(Decimal(p), s) for p, s in levels(book["bids"])] == sorted(ref["bids"].items(), reverse=True)
    assert ws.sent == []


def test_update_orders_is_unchanged_for_existing_callers():
    client = make_client()
    existing = [{"price": "1", "size": "1"}]
    client.update_orders([{"price": "2", "size": "3"}, {"price": "1", "size": "0"}], existing)
    assert existing == [{"price": "2", "size": "3"}]
