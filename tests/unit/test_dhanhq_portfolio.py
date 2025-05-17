from json import dumps as json_dumps
from unittest.mock import patch

import pytest

from dhanhq import DhanContext
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhanhq import dhanhq

class TestDhanhq_Portfolio:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_positions(self, mock_read_request, dhanhq_obj):
        dhanhq_obj.get_positions()
        mock_read_request.assert_called_once_with('/positions')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_holdings(self, mock_read_request, dhanhq_obj):
        dhanhq_obj.get_holdings()
        mock_read_request.assert_called_once_with('/holdings')

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_convert_position(self, mock_create_request, dhanhq_obj):
        dhanhq_obj.convert_position("from_product_type", "exchange_segment", "position_type", "security_id", "convert_qty", "to_product_type")
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == '/positions/convert'
