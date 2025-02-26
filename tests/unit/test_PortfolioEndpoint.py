from unittest.mock import patch

from dhanhq.constants import ExchangeSegment, PositionType, ProductType


class TestPortfolioEndpoint:
    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_positions(self, mock_read_request, dhanhq_obj):
        portfolioEndpoint = dhanhq_obj.portfolioEndpoint
        portfolioEndpoint.get_positions()
        mock_read_request.assert_called_once_with('/positions')

    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_holdings(self, mock_read_request, dhanhq_obj):
        portfolioEndpoint = dhanhq_obj.portfolioEndpoint
        portfolioEndpoint.get_holdings()
        mock_read_request.assert_called_once_with('/holdings')

    @patch("dhanhq.http.DhanHTTP.post")
    def test_convert_position(self, mock_create_request, dhanhq_obj):
        portfolioEndpoint = dhanhq_obj.portfolioEndpoint
        portfolioEndpoint.convert_position(ProductType.CNC, ExchangeSegment.NSE_EQ, PositionType.CLOSED, "security_id", "convert_qty", ProductType.INTRADAY)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == '/positions/convert'
