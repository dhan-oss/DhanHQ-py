from json import dumps as json_dumps
from unittest.mock import patch

import pytest

from dhanhq import DhanContext
from dhanhq.constants.exchange_segment import ExchangeSegment
from dhanhq.constants.position_type import PositionType
from dhanhq.constants.product_type import ProductType
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhancore import DhanCore

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
        dhanhq_obj.convert_position(ProductType.CNC, ExchangeSegment.NSE_EQ, PositionType.CLOSED, "security_id", "convert_qty", ProductType.INTRADAY)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == '/positions/convert'
