import asyncio
import json
from contextlib import suppress
from typing import Any, Awaitable, Callable, Mapping, Optional

try:
    from websockets.asyncio.client import connect as websocket_connect
except ImportError:  # pragma: no cover - compatibility with websockets 12.x
    from websockets.client import connect as websocket_connect


OrderBookMessageHandler = Callable[[int, Mapping[str, Any], bool], Awaitable[None]]


class PaperOrderBookListener:
    def __init__(
        self,
        market_id: int,
        ws_url: str,
        on_order_book_message: OrderBookMessageHandler,
        *,
        initial_snapshot_timeout: float = 10.0,
    ) -> None:
        self.market_id = market_id
        self.ws_url = ws_url
        self.on_order_book_message = on_order_book_message
        self.initial_snapshot_timeout = initial_snapshot_timeout

        self._task: Optional[asyncio.Task] = None
        self._websocket = None
        self._initial_snapshot: Optional[asyncio.Future] = None
        self._subscribed = False

    async def start(self) -> None:
        if self._task is not None and not self._task.done():
            return

        loop = asyncio.get_running_loop()
        self._initial_snapshot = loop.create_future()
        self._task = asyncio.create_task(self._run())
        self._task.add_done_callback(self._consume_task_exception)

        try:
            await asyncio.wait_for(
                self._initial_snapshot,
                timeout=self.initial_snapshot_timeout,
            )
        except Exception:
            await self.stop()
            raise

    async def stop(self) -> None:
        task = self._task
        websocket = self._websocket

        if websocket is not None:
            with suppress(Exception):
                await websocket.close()

        if task is not None:
            if not task.done():
                task.cancel()
            with suppress(asyncio.CancelledError, Exception):
                await task

        self._task = None
        self._websocket = None
        self._subscribed = False

    async def _run(self) -> None:
        try:
            async with websocket_connect(self.ws_url) as websocket:
                self._websocket = websocket

                async for raw_message in websocket:
                    await self._handle_raw_message(raw_message)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self._fail_initial_snapshot(exc)
            raise
        finally:
            self._websocket = None
            self._fail_initial_snapshot(
                RuntimeError(
                    f"websocket closed before market {self.market_id} snapshot"
                )
            )

    async def _handle_raw_message(self, raw_message: Any) -> None:
        if isinstance(raw_message, bytes):
            raise TypeError(
                "received binary websocket frame; paper client only supports "
                "JSON encoding (ensure ws URL includes ?encoding=json)"
            )
        message = json.loads(raw_message)
        message_type = message.get("type")

        if message_type == "connected":
            await self._send_subscribe()
            return

        if message_type == "ping":
            await self._send_json({"type": "pong"})
            return

        if message_type not in ("subscribed/order_book", "update/order_book"):
            return

        if self._message_market_id(message) != self.market_id:
            return

        order_book = message.get("order_book")
        if not isinstance(order_book, Mapping):
            raise ValueError("order book websocket message missing order_book payload")

        is_snapshot = message_type == "subscribed/order_book"
        await self.on_order_book_message(self.market_id, order_book, is_snapshot)
        if is_snapshot:
            self._resolve_initial_snapshot()

    async def _send_subscribe(self) -> None:
        if self._subscribed:
            return
        await self._send_json(
            {"type": "subscribe", "channel": f"order_book/{self.market_id}"}
        )
        self._subscribed = True

    async def _send_json(self, message: Mapping[str, Any]) -> None:
        if self._websocket is None:
            return
        await self._websocket.send(json.dumps(message))

    def _resolve_initial_snapshot(self) -> None:
        if self._initial_snapshot is not None and not self._initial_snapshot.done():
            self._initial_snapshot.set_result(None)

    def _fail_initial_snapshot(self, exc: Exception) -> None:
        if self._initial_snapshot is not None and not self._initial_snapshot.done():
            self._initial_snapshot.set_exception(exc)

    @staticmethod
    def _consume_task_exception(task: asyncio.Task) -> None:
        if task.cancelled():
            return
        with suppress(Exception):
            task.exception()

    @staticmethod
    def _message_market_id(message: Mapping[str, Any]) -> Optional[int]:
        channel = message.get("channel")
        if not isinstance(channel, str):
            return None

        for separator in (":", "/"):
            prefix = f"order_book{separator}"
            if channel.startswith(prefix):
                try:
                    return int(channel[len(prefix) :])
                except ValueError:
                    return None

        return None
