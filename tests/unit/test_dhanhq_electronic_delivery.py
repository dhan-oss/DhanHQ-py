from json import dumps as json_dumps
from unittest.mock import patch

import pytest

from dhanhq import DhanContext
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhanhq import dhanhq

class TestDhanhq_ElectronicDelivery:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_generate_tpin_for_success(self, mock_read_request, dhanhq_obj):
        mock_read_request.return_value = { 'status': DhanHTTP.HttpResponseStatus.SUCCESS.value, 'remarks': '', 'data': '', }
        json_response = dhanhq_obj.generate_tpin()
        mock_read_request.assert_called_once_with('/edis/tpin')
        assert json_response['remarks'] == dhanhq.OTP_SENT # ToDo: Ideally, response.data should be set so
        assert json_response['data'] == ''

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_generate_tpin_for_failure(self, mock_read_request, dhanhq_obj):
        mock_read_request.return_value = {
            'status': DhanHTTP.HttpResponseStatus.FAILURE.value,
            'remarks': {
                    'error_code': 'HTPP500',
                    'error_type': 'Internal Server Error',
                    'error_message': 'HTPP500:Internal Server Error'
                },
            'data': '', }
        json_response = dhanhq_obj.generate_tpin()
        mock_read_request.assert_called_once_with('/edis/tpin')
        assert json_response['remarks'].startswith('status code :')
        assert json_response['data'] == ''

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    @patch("dhanhq.dhanhq._save_as_temp_html_file_and_open_in_browser")
    def test_open_browser_for_tpin_success(self, mock_save_and_open, mock_create_request, dhanhq_obj):
        # print(mock_create_request)
        # print(mock_save_and_open)
        mock_create_request.return_value = {
            'status': DhanHTTP.HttpResponseStatus.SUCCESS.value,
            'data': '{"edisFormHtml": "<html></html>"}'
        }
        response = dhanhq_obj.open_browser_for_tpin('isin', 1, 'exchange')
        assert response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        mock_save_and_open.assert_called_once()

    @patch('dhanhq.dhan_http.DhanHTTP.post')
    @patch("dhanhq.dhanhq._save_as_temp_html_file_and_open_in_browser")
    def test_open_browser_for_tpin_failure(self, mock_save_and_open, mock_create_request, dhanhq_obj):
        mock_create_request.return_value = {
            'status': DhanHTTP.HttpResponseStatus.FAILURE.value,
            'data': ''
        }
        response = dhanhq_obj.open_browser_for_tpin('isin', 1, 'exchange')
        assert response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value
        mock_save_and_open.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_edis_inquiry(self, mock_read_request, dhanhq_obj):
        isin = "123"
        endpoint = f'/edis/inquire/{isin}'
        dhanhq_obj.edis_inquiry(isin)
        mock_read_request.assert_called_once_with(endpoint)
