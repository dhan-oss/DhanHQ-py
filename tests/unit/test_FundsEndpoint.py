from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, ProductType, TransactionType
from dhanhq.dto.compute_margin_request import ComputeMarginRequest


class TestFundsEndpoint:
    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_fund_limits(self, mock_read_request, dhanhq_obj):
        fundsEndpoint = dhanhq_obj.fundsEndpoint
        endpoint = '/fundlimit'
        fundsEndpoint.get_fund_limits()
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.http.DhanHTTP.post")
    def test_margin_calculator(self, mock_create_request, dhanhq_obj):
        endpoint = '/margincalculator'
        req_params = ComputeMarginRequest(security_id="123",
                                          exchange_segment=ExchangeSegment.BSE_EQ,
                                          transaction_type=TransactionType.SELL,
                                          quantity=100,
                                          product_type=ProductType.CNC,
                                          price=99.99)
        dhanhq_obj.fundsEndpoint.compute_margin_info(req_params)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint
