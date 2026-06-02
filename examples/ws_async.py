"""Async usage of :class:`lighter.WsClient`.

Reach for ``run_async()`` (instead of ``run()``) when you already have
an asyncio program — e.g. a trading bot that also makes REST calls,
maintains other WebSocket connections, or runs periodic tasks.
``run()`` is just ``asyncio.run(run_async())`` and cannot be called
from inside a running event loop.

This example shows the two things sync mode cannot do:

1. **Async callbacks.** Handlers may be ``async def`` and can ``await``
   coroutines directly (e.g. ``await client.send_tx(...)`` or an
   ``aiohttp`` REST call) without spawning threads.
2. **Concurrency with other async work.** ``run_async()`` shares the
   loop with the rest of your program — here we run a periodic stats
   task alongside the WebSocket consumer via :func:`asyncio.gather`.
"""

import asyncio
import logging

import lighter

logging.basicConfig(level=logging.INFO)


class Counters:
    book_updates = 0
    account_updates = 0


async def on_order_book(message):
    Counters.book_updates += 1
    # Async callbacks can await arbitrary coroutines — e.g. an aiohttp
    # REST call, a database write, or ``await client.send_tx(...)`` to
    # react to a book change with an order. A sync callback would have
    # to schedule that work on a separate thread/loop.
    bids = (message.get("order_book") or {}).get("bids") or []
    logging.info("order book %s: %d bid levels", message["channel"], len(bids))


async def on_account(message):
    Counters.account_updates += 1
    logging.info("account %s update", message["channel"])


async def log_stats():
    """Independent task running on the same loop as the ws client."""
    while True:
        await asyncio.sleep(10)
        logging.info(
            "stats: %d book updates, %d account updates",
            Counters.book_updates,
            Counters.account_updates,
        )


async def main():
    client = lighter.WsClient()
    for market_id in [0, 1]:
        client.subscribe(f"order_book/{market_id}", on_update=on_order_book)
    for account_id in [1, 2]:
        client.subscribe(f"account_all/{account_id}", on_update=on_account)

    # ``run_async()`` runs forever; ``log_stats()`` runs in parallel on
    # the same loop. In a real app, replace ``log_stats`` with whatever
    # other async work your bot already does.
    await asyncio.gather(
        client.run_async(),
        log_stats(),
    )


if __name__ == "__main__":
    asyncio.run(main())
