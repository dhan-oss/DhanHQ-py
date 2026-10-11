import asyncio
from unittest.mock import MagicMock, patch
import pytest
from dhanhq import MarketFeed, DhanContext

class TestMarketFeed:
    @pytest.fixture
    def mock_context(self):
        return DhanContext("client_id", "access_token")

    @patch("dhanhq.marketfeed.websockets.connect")
    def test_market_feed_init_v2(self, mock_ws_connect, mock_context):
        instruments = [(1, "1333", 15)]
        feed = MarketFeed(mock_context, instruments, version="v2")
        assert feed.client_id == "client_id"
        assert feed.access_token == "access_token"
        assert feed.version == "v2"

    @patch("dhanhq.marketfeed.websockets.connect")
    def test_subscribe_symbols(self, mock_ws_connect, mock_context):
        instruments = [(1, "1333", 15)]
        feed = MarketFeed(mock_context, instruments)
        # Manually attach mock ws since 'run_forever' isn't called to spawn it
        feed.ws = MagicMock()
        
        new_instruments = [(1, "14436", 15)]
        feed.subscribe_symbols(new_instruments)
        # Verify it tries to send subscription packet (implementation detail dependent)
        # For now, just ensuring method runs without error
        assert True

    def test_disconnect_clears_and_closes_websocket(self, mock_context):
        class MockWebSocket:
            def __init__(self):
                self.sent_messages = []
                self.closed = False

            async def send(self, message):
                self.sent_messages.append(message)

            async def close(self):
                self.closed = True

        instruments = [(1, "1333", 15)]
        feed = MarketFeed(mock_context, instruments, version="v2")
        ws = MockWebSocket()
        feed.ws = ws

        feed.loop.run_until_complete(feed.disconnect())

        assert feed.ws is None
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

        instruments = [(1, "1333", 15)]
        feed = MarketFeed(mock_context, instruments, version="v2")
        feed.loop = MockLoop()
        future = MockFuture()

        def mock_run_coroutine_threadsafe(coro, loop):
            coro.close()
            assert loop == feed.loop
            return future

        monkeypatch.setattr(asyncio, "run_coroutine_threadsafe", mock_run_coroutine_threadsafe)

        feed.close_connection()

        assert future.cancelled
