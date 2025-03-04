from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, InstrumentType
from dhanhq.http import DhanHTTP


class TestMarketFeedEndpoint:

    @patch("dhanhq.http.DhanHTTP.post")
    def test_ticker_data(self, mock_create_request, dhanhq_obj):
        marketFeedEndpoint = dhanhq_obj.marketFeedEndpoint
        endpoint = '/marketfeed/ltp'
        securities = {
            'exchange_segment1': 'sec1',
            'exchange_segment2': 'sec2'
        }
        expected_data = {'sec1': 99.9, 'sec2':88.8}
        mock_create_request.return_value = expected_data
        data = marketFeedEndpoint.ticker_data(securities)
        mock_create_request.assert_called_once()
        assert data == expected_data
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
        expected_data = {'open': 99.9, 'high': 100, 'low': 90, 'close': 101}
        mock_create_request.return_value = expected_data
        data = marketFeedEndpoint.ohlc_data(securities)
        mock_create_request.assert_called_once()
        assert set(data.keys()) == {'open', 'high', 'low', 'close'}
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
        expected_data = { 'quote': 100 }
        mock_create_request.return_value = expected_data
        data = marketFeedEndpoint.quote_data(securities)
        mock_create_request.assert_called_once()
        assert data['quote'] == 100
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities
