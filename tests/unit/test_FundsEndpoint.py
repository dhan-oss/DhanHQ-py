from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, ProductType, TransactionType


class TestFundsEndpoint:
    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_fund_limits(self, mock_read_request, dhanhq_obj):
        fundsEndpoint = dhanhq_obj.fundsEndpoint
        endpoint = '/fundlimit'
        fundsEndpoint.get_fund_limits()
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.http.DhanHTTP.post")
    def test_margin_calculator(self, mock_create_request, dhanhq_obj):
        fundsEndpoint = dhanhq_obj.fundsEndpoint
        endpoint = '/margincalculator'
        quantity=100
        price = 99.99
        fundsEndpoint.margin_calculator("security_id", ExchangeSegment.NSE_EQ, TransactionType.BUY,
                                     quantity, ProductType.MARGIN, price)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint
