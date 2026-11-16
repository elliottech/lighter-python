"""Regression tests for non-object JSON WS frames (issue #123). No network."""

import json
import unittest
from unittest.mock import AsyncMock, Mock

from lighter.ws_client import WsClient


NON_OBJECT_FRAMES = ('"heartbeat"', 'null', '[]', '42', 'true')


class TestWsClientNonObjectFrames(unittest.TestCase):
    def setUp(self):
        self.unhandled = Mock()
        self.client = WsClient(
            ws_url="wss://example.invalid/stream",
            order_book_ids=[1],
            on_unhandled_message=self.unhandled,
        )

    def test_sync_ignores_non_object_json(self):
        ws = Mock()
        for frame in NON_OBJECT_FRAMES:
            with self.subTest(frame=frame):
                self.client.on_message(ws, frame)
        self.unhandled.assert_not_called()
        ws.send.assert_not_called()

    def test_sync_ping_responds_normally(self):
        ws = Mock()
        self.client.on_message(ws, json.dumps({"type": "ping"}))
        ws.send.assert_called_once_with(json.dumps({"type": "pong"}))


class TestWsClientAsyncNonObjectFrames(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.unhandled = Mock()
        self.client = WsClient(
            ws_url="wss://example.invalid/stream",
            order_book_ids=[1],
            on_unhandled_message=self.unhandled,
        )

    async def test_async_ignores_non_object_json(self):
        ws = Mock()
        ws.send = AsyncMock()
        for frame in NON_OBJECT_FRAMES:
            with self.subTest(frame=frame):
                await self.client.on_message_async(ws, frame)
        self.unhandled.assert_not_called()
        ws.send.assert_not_awaited()

    async def test_async_ping_responds_normally(self):
        ws = Mock()
        ws.send = AsyncMock()
        await self.client.on_message_async(ws, json.dumps({"type": "ping"}))
        ws.send.assert_awaited_once_with(json.dumps({"type": "pong"}))


if __name__ == "__main__":
    unittest.main()
