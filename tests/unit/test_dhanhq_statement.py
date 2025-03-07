from json import dumps as json_dumps
from unittest.mock import patch

import pytest

from dhanhq import DhanContext
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhanhq import dhanhq


class TestDhanhq_Statement:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_trade_book_without_orderid(self, mock_read_request, dhanhq_obj):
        endpoint = '/trades/'
        dhanhq_obj.get_trade_book()
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_trade_book_with_orderid(self, mock_read_request, dhanhq_obj):
        order_id = "order_id"
        endpoint = f'/trades/{order_id}'
        dhanhq_obj.get_trade_book(order_id)
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_trade_history(self, mock_read_request, dhanhq_obj):
        from_date = "from_date"
        to_date = "to_date"
        page_number = "page_number"
        endpoint = f'/trades/{from_date}/{to_date}/{page_number}'
        dhanhq_obj.get_trade_history(from_date,to_date,page_number)
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_ledger_report(self, mock_read_request, dhanhq_obj):
        from_date = "from_date"
        to_date = "to_date"
        endpoint = f'/ledger?from-date={from_date}&to-date={to_date}'
        dhanhq_obj.ledger_report(from_date,to_date)
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_intraday_minute_data(self, mock_create_request, dhanhq_obj):
        endpoint = f'/charts/intraday'
        security_id="security_id"
        exchange_segment="exchange_segment"
        instrument_type="instrument_type"
        from_date="from_date"
        to_date="to_date"
        mock_create_request.return_value = { 'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.intraday_minute_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_intraday_minute_data_fails_for_bad_interval_input(self, mock_create_request, dhanhq_obj):
        security_id="security_id"
        exchange_segment="exchange_segment"
        instrument_type="instrument_type"
        from_date="from_date"
        to_date="to_date"
        interval=100
        json_response = dhanhq_obj.intraday_minute_data(security_id, exchange_segment, instrument_type, from_date, to_date, interval)
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value
        mock_create_request.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_historical_daily_data(self, mock_create_request, dhanhq_obj):
        endpoint = f'/charts/historical'
        security_id='security_id'
        exchange_segment='exchange_segment'
        instrument_type='instrument_type'
        from_date="from_date"
        to_date="to_date"
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.historical_daily_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_historical_daily_data_fails_for_bad_expiry_code(self, mock_create_request, dhanhq_obj):
        security_id='security_id'
        exchange_segment='exchange_segment'
        instrument_type='instrument_type'
        from_date="from_date"
        to_date="to_date"
        bad_expiry_code=99
        json_response = dhanhq_obj.historical_daily_data(security_id, exchange_segment, instrument_type, from_date, to_date,bad_expiry_code)
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value
        mock_create_request.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_ticker_data(self, mock_create_request, dhanhq_obj):
        endpoint = '/marketfeed/ltp'
        securities = {
            'exchange_segment1': 'security_id1',
            'exchange_segment2': 'security_id2'
        }
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.ticker_data(securities)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_ohlc_data(self, mock_create_request, dhanhq_obj):
        endpoint = '/marketfeed/ohlc'
        securities = {
            'exchange_segment1': 'security_id1',
            'exchange_segment2': 'security_id2'
        }
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.ohlc_data(securities)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_quote_data(self, mock_create_request, dhanhq_obj):
        endpoint = '/marketfeed/quote'
        securities = {
            'exchange_segment1': 'security_id1',
            'exchange_segment2': 'security_id2'
        }
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.quote_data(securities)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_option_chain(self, mock_create_request, dhanhq_obj):
        endpoint = '/optionchain'
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.option_chain("under_security_id", "under_exchange_segment", "expiry")
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_expiry_list(self, mock_create_request, dhanhq_obj):
        endpoint = '/optionchain/expirylist'
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.expiry_list("under_security_id", "under_exchange_segment")
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
