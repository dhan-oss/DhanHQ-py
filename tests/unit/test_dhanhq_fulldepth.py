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
