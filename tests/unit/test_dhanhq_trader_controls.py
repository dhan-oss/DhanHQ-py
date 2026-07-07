from json import dumps as json_dumps
from unittest.mock import patch

import pytest

from dhanhq import DhanContext
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhanhq import dhanhq


class TestDhanhq_TraderControls:
    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_kill_switch(self, mock_post_request, dhanhq_obj):
        action = "action"
        endpoint = f'/killswitch?killSwitchStatus={action.upper()}'
        dhanhq_obj.kill_switch(action)
        mock_post_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_set_pnl_exit(self, mock_post_request, dhanhq_obj):
        dhanhq_obj.set_pnl_exit(1500, 500, ["INTRADAY", "DELIVERY"], enable_kill_switch=True)
        mock_post_request.assert_called_once()
        assert mock_post_request.call_args[0][0] == '/pnlExit'
        payload = mock_post_request.call_args[0][1]
        assert payload["profitValue"] == 1500.0
        assert payload["lossValue"] == 500.0
        assert payload["productType"] == ["INTRADAY", "DELIVERY"]
        assert payload["enableKillSwitch"] is True

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_pnl_exit(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_pnl_exit()
        mock_get_request.assert_called_once_with('/pnlExit')

    @patch("dhanhq.dhan_http.DhanHTTP.delete")
    def test_stop_pnl_exit(self, mock_delete_request, dhanhq_obj):
        dhanhq_obj.stop_pnl_exit()
        mock_delete_request.assert_called_once_with('/pnlExit')
