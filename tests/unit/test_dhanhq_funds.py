from unittest.mock import patch

from dhanhq.constants import ExchangeSegment, ProductType, TransactionType


class TestDhanhq_Funds:
    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_fund_limits(self, mock_read_request, dhanhq_obj):
        endpoint = '/fundlimit'
        dhanhq_obj.get_fund_limits()
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.http.DhanHTTP.post")
    def test_margin_calculator(self, mock_create_request, dhanhq_obj):
        endpoint = '/margincalculator'
        quantity=100
        price = 99.99
        dhanhq_obj.margin_calculator("security_id", ExchangeSegment.NSE_EQ, TransactionType.BUY,
                                     quantity, ProductType.MARGIN, price)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint
