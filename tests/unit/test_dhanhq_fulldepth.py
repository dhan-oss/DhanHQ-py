from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from dhanhq import FullDepth, DhanContext

class TestFullDepth:
    @pytest.mark.parametrize("close_error", [ConnectionClosedOK, ConnectionClosedError])
    def test_close_connection_handles_closed_socket(self, mock_context, close_error):
        depth = FullDepth(mock_context, [(1, "1333")])
        websocket = MagicMock()
        websocket.send = AsyncMock(side_effect=close_error(None, None))
        websocket.close = AsyncMock()
        depth.ws = websocket
        try:
            depth.close_connection()
            websocket.close.assert_awaited_once()
            assert depth.ws is None
        finally:
            depth.loop.close()

    @pytest.mark.parametrize("send_fails", [False, True])
    def test_close_connection_closes_socket(self, mock_context, send_fails):
        depth = FullDepth(mock_context, [(1, "1333")])
        websocket = MagicMock()
        websocket.send = AsyncMock()
        websocket.close = AsyncMock()
        depth.ws = websocket
        if send_fails:
            websocket.send.side_effect = RuntimeError("send failed")
        try:
            if send_fails:
                with pytest.raises(RuntimeError, match="send failed"):
                    depth.close_connection()
            else:
                depth.close_connection()
                assert websocket.send.await_count == 2
            websocket.close.assert_awaited_once()
            assert depth.ws is None
            depth.close_connection()
            websocket.close.assert_awaited_once()
        finally:
            depth.loop.close()

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
