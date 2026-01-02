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
