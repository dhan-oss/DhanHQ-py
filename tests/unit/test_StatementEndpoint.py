from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, InstrumentType
from dhanhq.http import DhanHTTP


class TestStatementEndpoint:
    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_trade_book_without_orderid(self, mock_read_request, dhanhq_obj):
        statementEndpoint = dhanhq_obj.statementEndpoint
        endpoint = '/trades/'
        statementEndpoint.get_trade_book()
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_trade_book_with_orderid(self, mock_read_request, dhanhq_obj):
        statementEndpoint = dhanhq_obj.statementEndpoint
        order_id = "order_id"
        endpoint = f'/trades/{order_id}'
        statementEndpoint.get_trade_book(order_id)
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_trade_history(self, mock_read_request, dhanhq_obj):
        statementEndpoint = dhanhq_obj.statementEndpoint
        from_date = "from_date"
        to_date = "to_date"
        page_number = "page_number"
        endpoint = f'/trades/{from_date}/{to_date}/{page_number}'
        statementEndpoint.get_trade_history(from_date,to_date,page_number)
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.http.DhanHTTP.get")
    def test_ledger_report(self, mock_read_request, dhanhq_obj):
        statementEndpoint = dhanhq_obj.statementEndpoint
        from_date = "from_date"
        to_date = "to_date"
        endpoint = f'/ledger?from-date={from_date}&to-date={to_date}'
        statementEndpoint.ledger_report(from_date,to_date)
        mock_read_request.assert_called_once_with(endpoint)
