from unittest.mock import patch

from dhanhq.constants import ExchangeSegment, InstrumentType
from dhanhq.http import DhanHTTP


class TestHistoricalDataEndpoint:

    @patch("dhanhq.http.DhanHTTP.post")
    def test_intraday_minute_data(self, mock_create_request, dhanhq_obj):
        historicalDataEndpoint = dhanhq_obj.historicalDataEndpoint
        endpoint = f'/charts/intraday'
        security_id="security_id"
        exchange_segment=ExchangeSegment.NSE_EQ
        instrument_type=InstrumentType.EQUITY
        from_date="from_date"
        to_date="to_date"
        mock_create_request.return_value = { 'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = historicalDataEndpoint.intraday_minute_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.post")
    def test_historical_daily_data(self, mock_create_request, dhanhq_obj):
        historicalDataEndpoint = dhanhq_obj.historicalDataEndpoint
        endpoint = f'/charts/historical'
        security_id='security_id'
        exchange_segment=ExchangeSegment.NSE_EQ
        instrument_type=InstrumentType.INDEX
        from_date="from_date"
        to_date="to_date"
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = historicalDataEndpoint.historical_daily_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
