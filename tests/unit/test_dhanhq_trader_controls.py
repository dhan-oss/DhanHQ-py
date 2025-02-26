from unittest.mock import patch

from dhanhq.constants import KillSwitchStatus


class TestDhanhq_TraderControls:
    @patch("dhanhq.http.DhanHTTP.post")
    def test_kill_switch(self, mock_post_request, dhanhq_obj):
        action = KillSwitchStatus.ACTIVATE
        endpoint = f'/killswitch?killSwitchStatus={action.name}'
        dhanhq_obj.kill_switch(action)
        mock_post_request.assert_called_once_with(endpoint)
