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
