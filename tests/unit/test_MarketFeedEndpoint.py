from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, InstrumentType
from dhanhq.http import DhanHTTP


class TestMarketFeedEndpoint:

    @patch("dhanhq.http.DhanHTTP.post")
    def test_ticker_data(self, mock_create_request, dhanhq_obj):
        marketFeedEndpoint = dhanhq_obj.marketFeedEndpoint
        endpoint = '/marketfeed/ltp'
        securities = {
            'exchange_segment1': 'security_id1',
            'exchange_segment2': 'security_id2'
        }
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = marketFeedEndpoint.ticker_data(securities)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities

    @patch("dhanhq.http.DhanHTTP.post")
    def test_ohlc_data(self, mock_create_request, dhanhq_obj):
        marketFeedEndpoint = dhanhq_obj.marketFeedEndpoint
        endpoint = '/marketfeed/ohlc'
        securities = {
            'exchange_segment1': 'security_id1',
            'exchange_segment2': 'security_id2'
        }
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = marketFeedEndpoint.ohlc_data(securities)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities

    @patch("dhanhq.http.DhanHTTP.post")
    def test_quote_data(self, mock_create_request, dhanhq_obj):
        marketFeedEndpoint = dhanhq_obj.marketFeedEndpoint
        endpoint = '/marketfeed/quote'
        securities = {
            'exchange_segment1': 'security_id1',
            'exchange_segment2': 'security_id2'
        }
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = marketFeedEndpoint.quote_data(securities)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities
