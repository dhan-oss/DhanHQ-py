import asyncio
import struct
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from dhanhq import DhanContext, MarketFeed


def _ticker_packet():
    return struct.pack("<BHBIfI", 2, 0, 1, 1333, 100.5, 1700000000)


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

    @pytest.mark.asyncio
    async def test_run_async_receives_messages_sync_callback(self, mock_context):
        messages_received = []

        def on_message(feed_instance, data):
            messages_received.append(data)
            if len(messages_received) == 1:
                feed_instance.close_connection()

        feed = MarketFeed(mock_context, [(1, "1333", 15)], on_message=on_message)

        mock_ws = AsyncMock()
        mock_ws.recv.return_value = _ticker_packet()
        mock_ws.state = 1
        mock_ws.closed = False
        feed.ws = mock_ws

        with patch.object(feed, "connect", AsyncMock()) as mock_connect:
            await feed.run_async()
            mock_connect.assert_not_called()

        assert len(messages_received) == 1
        assert messages_received[0]["type"] == "Ticker Data"
        assert messages_received[0]["security_id"] == 1333
        assert feed._running is False

    @pytest.mark.asyncio
    async def test_run_async_receives_messages_async_callback(self, mock_context):
        messages_received = []

        async def on_message(feed_instance, data):
            messages_received.append(data)
            await feed_instance.disconnect()

        feed = MarketFeed(mock_context, [(1, "1333", 15)], on_message=on_message)

        mock_ws = AsyncMock()
        mock_ws.recv.return_value = _ticker_packet()
        mock_ws.state = 1
        mock_ws.closed = False
        feed.ws = mock_ws

        with patch.object(feed, "connect", AsyncMock()):
            await feed.run_async()

        assert len(messages_received) == 1
        assert messages_received[0]["type"] == "Ticker Data"
        assert feed._running is False

    @pytest.mark.asyncio
    async def test_run_async_when_connect_called_first(self, mock_context):
        # Reproduces issue #75 scenario: user calls await feed.connect(), then await feed.run_async()
        connected = []
        messages_received = []

        def on_connect(feed_instance):
            connected.append(True)

        def on_message(feed_instance, data):
            messages_received.append(data)
            feed_instance.close_connection()

        feed = MarketFeed(
            mock_context,
            [(1, "1333", 15)],
            on_connect=on_connect,
            on_message=on_message,
        )

        mock_ws = AsyncMock()
        mock_ws.recv.return_value = _ticker_packet()
        mock_ws.state = 1
        mock_ws.closed = False

        with patch("dhanhq.marketfeed.websockets.connect", AsyncMock(return_value=mock_ws)):
            await feed.connect()
            assert len(connected) == 1
            assert feed.ws is mock_ws

            # Now run_async should continue on the open connection and process messages
            await feed.run_async()

        assert len(messages_received) == 1
        assert feed._running is False

    @pytest.mark.asyncio
    async def test_run_async_connects_if_not_connected(self, mock_context):
        messages_received = []

        def on_message(feed_instance, data):
            messages_received.append(data)
            feed_instance.close_connection()

        feed = MarketFeed(mock_context, [(1, "1333", 15)], on_message=on_message)

        mock_ws = AsyncMock()
        mock_ws.recv.return_value = _ticker_packet()
        mock_ws.state = 1
        mock_ws.closed = False

        with patch("dhanhq.marketfeed.websockets.connect", AsyncMock(return_value=mock_ws)):
            await feed.run_async()

        assert len(messages_received) == 1
        assert feed._running is False

    @pytest.mark.asyncio
    async def test_run_async_cancellation_cleans_up(self, mock_context):
        feed = MarketFeed(mock_context, [(1, "1333", 15)])
        mock_ws = AsyncMock()

        async def slow_recv():
            await asyncio.sleep(10)
            return _ticker_packet()

        mock_ws.recv.side_effect = slow_recv
        mock_ws.state = 1
        mock_ws.closed = False
        feed.ws = mock_ws

        task = asyncio.create_task(feed.run_async())
        await asyncio.sleep(0.01)
        assert feed._running is True

        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        assert feed._running is False
        mock_ws.close.assert_awaited()

    @pytest.mark.asyncio
    async def test_run_async_error_callback(self, mock_context):
        errors = []

        def on_error(feed_instance, err):
            errors.append(err)
            feed_instance.close_connection()

        feed = MarketFeed(mock_context, [(1, "1333", 15)], on_error=on_error)
        mock_ws = AsyncMock()
        mock_ws.recv.side_effect = RuntimeError("network fault")
        mock_ws.state = 1
        mock_ws.closed = False
        feed.ws = mock_ws

        await feed.run_async()
        assert len(errors) == 1
        assert str(errors[0]) == "network fault"
        assert feed._running is False

    @pytest.mark.asyncio
    async def test_disconnect_sets_running_false_and_triggers_on_close(self, mock_context):
        closed = []

        async def on_close(feed_instance):
            closed.append(True)

        feed = MarketFeed(mock_context, [(1, "1333", 15)], on_close=on_close)
        feed._running = True
        mock_ws = AsyncMock()
        mock_ws.state = 1
        mock_ws.closed = False
        feed.ws = mock_ws

        await feed.disconnect()
        assert feed._running is False
        assert len(closed) == 1
        mock_ws.close.assert_awaited_once()
