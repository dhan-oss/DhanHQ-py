from unittest.mock import patch

from dhanhq.api import DhanCore
from dhanhq.api.ondemand import SecurityEndpoint
from dhanhq.http import DhanHTTP


class TestSecurityEndpoint:
    @patch("dhanhq.http.DhanHTTP.get")
    def test_generate_tpin_for_success(self, mock_read_request, dhanhq_obj):
        securityEndpoint = dhanhq_obj.securityEndpoint
        mock_read_request.return_value = 'Request accepted for processing'
        json_response = securityEndpoint.generate_tpin()
        mock_read_request.assert_called_once_with('/edis/tpin')
        assert json_response == SecurityEndpoint.OTP_SENT

    @patch("dhanhq.http.DhanHTTP.post")
    @patch.object(SecurityEndpoint, "_save_as_temp_html_file_and_open_in_browser")
    def test_open_browser_for_tpin_success(self, mock_save_and_open, mock_create_request, dhanhq_obj):
        securityEndpoint = dhanhq_obj.securityEndpoint
        mock_create_request.return_value = {'dhanClientId': "1000000401", 'edisFormHtml': "!DOCTYPE html"}
        dict_response = securityEndpoint.open_browser_for_tpin('isin', 1, 'exchange')
        assert dict_response['edisFormHtml'] == "!DOCTYPE html"
        mock_save_and_open.assert_called_once()

    @patch("dhanhq.http.DhanHTTP.get")
    def test_edis_inquiry(self, mock_read_request, dhanhq_obj):
        securityEndpoint = dhanhq_obj.securityEndpoint
        isin = "123"
        endpoint = f'/edis/inquire/{isin}'
        securityEndpoint.edis_inquiry(isin)
        mock_read_request.assert_called_once_with(endpoint)
