import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from dhanhq import MarketFeed, DhanContext


class TestMarketFeedReconnectBackoff:
    """run()/_run_async() used to retry a dropped connection at a flat 1s
    cadence forever (no way for a caller to throttle it -- run() never
    returns/raises on a connection drop), and connect() called on_error
    then re-raised into the caller's own except, firing on_error twice
    per real failure. See the fix's PR description for the full
    diagnosis and the live incident it caused (HTTP 429 rate-limit
    hammered through instead of backed off from)."""

    @pytest.fixture
    def mock_context(self):
        return DhanContext("client_id", "access_token")

    async def _run_until(self, feed, n_sleeps):
        """Drive _run_async() until asyncio.sleep has been called n_sleeps
        times, then stop (real asyncio.sleep is mocked out so this is
        instant)."""
        sleeps = []

        async def fake_sleep(seconds):
            sleeps.append(seconds)
            if len(sleeps) >= n_sleeps:
                feed._running = False

        with patch("asyncio.sleep", fake_sleep):
            feed._running = True
            await feed._run_async()
        return sleeps

    @pytest.mark.asyncio
    async def test_backoff_grows_exponentially_and_caps_at_max(self, mock_context):
        errors = []
        feed = MarketFeed(mock_context, [(1, "1333", 15)], version="v2",
                          on_error=lambda inst, e: errors.append(str(e)))
        feed.reconnect_backoff_max = 8.0
        with patch("dhanhq.marketfeed.websockets.connect",
                   AsyncMock(side_effect=Exception("connection reset"))):
            sleeps = await self._run_until(feed, 5)
        assert sleeps == [1.0, 2.0, 4.0, 8.0, 8.0]
        assert len(errors) == 6  # initial connect() attempt + one per loop iteration

    @pytest.mark.asyncio
    async def test_rate_limited_error_parks_and_resets_growth(self, mock_context):
        feed = MarketFeed(mock_context, [(1, "1333", 15)], version="v2")
        feed.rate_limit_backoff_seconds = 30.0
        feed._reconnect_backoff = 8.0  # pretend it had already grown
        with patch("dhanhq.marketfeed.websockets.connect",
                   AsyncMock(side_effect=Exception("server rejected WebSocket connection: HTTP 429"))):
            sleeps = await self._run_until(feed, 1)
        assert sleeps == [30.0]
        assert feed._reconnect_backoff == feed.reconnect_backoff_base

    @pytest.mark.asyncio
    async def test_a_successful_message_resets_backoff_to_base(self, mock_context):
        feed = MarketFeed(mock_context, [(1, "1333", 15)], version="v2")
        feed._reconnect_backoff = 16.0

        async def one_shot_message():
            feed._running = False
            return {"LTP": "100.0"}

        with patch.object(feed, "connect", AsyncMock()), \
             patch.object(feed, "_is_ws_closed", return_value=False), \
             patch.object(feed, "get_instrument_data", one_shot_message):
            feed.ws = MagicMock()
            feed._running = True
            await feed._run_async()
        assert feed._reconnect_backoff == feed.reconnect_backoff_base

    @pytest.mark.asyncio
    async def test_connect_failure_calls_on_error_exactly_once(self, mock_context):
        calls = []
        feed = MarketFeed(mock_context, [(1, "1333", 15)], version="v2",
                          on_error=lambda inst, e: calls.append(e))
        with patch("dhanhq.marketfeed.websockets.connect",
                   AsyncMock(side_effect=Exception("boom"))):
            with pytest.raises(Exception, match="boom"):
                await feed.connect()
        assert calls == []  # connect() itself no longer logs -- caller does


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
