from json import dumps as json_dumps
from unittest.mock import patch

import pytest

from dhanhq import DhanContext
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhanhq import dhanhq


class TestDhanhq_Funds:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_fund_limits(self, mock_read_request, dhanhq_obj):
        endpoint = '/fundlimit'
        dhanhq_obj.get_fund_limits()
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_margin_calculator(self, mock_create_request, dhanhq_obj):
        endpoint = '/margincalculator'
        quantity=100
        price = 99.99
        dhanhq_obj.margin_calculator("security_id", "exchange_segment", "transaction_type",
                                     100, "product_type", price)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_margin_calculator_multi(self, mock_create_request, dhanhq_obj):
        endpoint = '/margincalculator/multi'
        scrip_list = [
            {"securityId": "26009", "exchangeSegment": "NSE_FNO", "transactionType": "BUY",
             "quantity": 50, "productType": "INTRADAY", "price": 45000.00},
            {"securityId": "26010", "exchangeSegment": "NSE_FNO", "transactionType": "SELL",
             "quantity": 50, "productType": "INTRADAY", "price": 45500.00}
        ]
        dhanhq_obj.margin_calculator_multi(scrip_list, include_position=True, include_order=False)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint
        payload = mock_create_request.call_args[0][1]
        assert payload["scripList"] == scrip_list
        assert payload["includePosition"] is True
        assert payload["includeOrder"] is False
