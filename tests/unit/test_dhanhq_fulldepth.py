import asyncio
from unittest.mock import MagicMock, patch
import pytest
from dhanhq import FullDepth, DhanContext

class TestFullDepth:
    @pytest.fixture
    def mock_context(self):
        return DhanContext("client_id", "access_token")

    @patch("dhanhq.fulldepth.websockets.connect")
    def test_full_depth_init(self, mock_ws_connect, mock_context):
        instruments = [(1, "1333")]
        depth = FullDepth(mock_context, instruments)
        assert depth.client_id == "client_id"
        assert depth.access_token == "access_token"
        assert depth.depth_level == 20 # default

    def test_disconnect_clears_and_closes_websocket(self, mock_context):
        class MockWebSocket:
            def __init__(self):
                self.sent_messages = []
                self.closed = False

            async def send(self, message):
                self.sent_messages.append(message)

            async def close(self):
                self.closed = True

        instruments = [(1, "1333")]
        depth = FullDepth(mock_context, instruments)
        ws = MockWebSocket()
        depth.ws = ws

        depth.loop.run_until_complete(depth.disconnect())

        assert depth.ws is None
        assert ws.closed
        assert len(ws.sent_messages) == 2

    def test_close_connection_cancels_disconnect_on_timeout(self, monkeypatch, mock_context):
        class MockFuture:
            def __init__(self):
                self.cancelled = False

            def result(self, timeout=None):
                assert timeout == 5
                raise TimeoutError

            def cancel(self):
                self.cancelled = True

        class MockLoop:
            def is_running(self):
                return True

        instruments = [(1, "1333")]
        depth = FullDepth(mock_context, instruments)
        depth.loop = MockLoop()
        future = MockFuture()

        def mock_run_coroutine_threadsafe(coro, loop):
            coro.close()
            assert loop == depth.loop
            return future

        monkeypatch.setattr(asyncio, "run_coroutine_threadsafe", mock_run_coroutine_threadsafe)

        depth.close_connection()

        assert future.cancelled
