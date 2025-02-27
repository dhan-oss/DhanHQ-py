from unittest.mock import patch

from dhanhq.constant import KillSwitchStatus


class TestDhanhq_TraderControls:
    @patch("dhanhq.http.DhanHTTP.post")
    def test_kill_switch(self, mock_post_request, dhanhq_obj):
        traderControlEndpoint = dhanhq_obj.traderControlEndpoint
        action = KillSwitchStatus.ACTIVATE
        endpoint = f'/killswitch?killSwitchStatus={action.name}'
        traderControlEndpoint.kill_switch(action)
        mock_post_request.assert_called_once_with(endpoint)
