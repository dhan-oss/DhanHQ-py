from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, InstrumentType
from dhanhq.http import DhanHTTP


class TestHistoricalDataEndpoint:

    def __stub_historical_data(self):
        return {
            "open": [3750, 3757.85, 3751.2, 3763.6, 3759.55],
            "high": [3750, 3757.9, 3763.6, 3765.2, 3763.15],
            "low": [3750, 3746.1, 3749.25, 3757, 3758.65],
            "close": [3750, 3751.25, 3763.6, 3760.85, 3759],
            "volume": [166, 53629, 34592, 20802, 11262, 17549],
            "timestamp": [1328845020, 1328845500, 1328845560, 1328845620, 1328845680]
        }

    @patch("dhanhq.http.DhanHTTP.post")
    def test_intraday_minute_data(self, mock_create_request, dhanhq_obj):
        historicalDataEndpoint = dhanhq_obj.historicalDataEndpoint
        endpoint = f'/charts/intraday'
        security_id="security_id"
        exchange_segment=ExchangeSegment.NSE_EQ
        instrument_type=InstrumentType.EQUITY
        from_date="from_date"
        to_date="to_date"
        mock_create_request.return_value = self.__stub_historical_data()

        dict_response = historicalDataEndpoint.intraday_minute_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        assert set(dict_response.keys()) == {"open", "high", "low", "close", "volume", "timestamp"}
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
        mock_create_request.return_value = self.__stub_historical_data()
        dict_response = historicalDataEndpoint.historical_daily_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        assert set(dict_response.keys()) == {"open", "high", "low", "close", "volume", "timestamp"}
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint
