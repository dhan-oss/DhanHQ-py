from unittest.mock import patch
import pytest
from dhanhq.dhan_http import DhanHTTP

class TestDhanhq_HistoricalData:
    
    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_expired_options_data_success(self, mock_create_request, dhanhq_obj):
        endpoint = '/charts/rollingoption'
        security_id = "13"
        exchange_segment = "NSE_FNO"
        instrument_type = "OPTIDX"
        expiry_flag = "MONTH"
        expiry_code = 1
        strike = "ATM"
        drv_option_type = "CALL"
        required_data = ["open", "high", "low", "close", "volume"]
        from_date = "2023-01-01"
        to_date = "2023-01-31"
        
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        
        json_response = dhanhq_obj.expired_options_data(
            security_id, exchange_segment, instrument_type, expiry_flag, 
            expiry_code, strike, drv_option_type, required_data, 
            from_date, to_date
        )
        
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        
        payload = mock_create_request.call_args[0][1]
        assert payload['securityId'] == security_id
        assert payload['exchangeSegment'] == exchange_segment
        assert payload['instrument'] == instrument_type
        assert payload['expiryFlag'] == expiry_flag
        assert payload['expiryCode'] == expiry_code
        assert payload['strike'] == strike
        assert payload['drvOptionType'] == drv_option_type
        assert payload['requiredData'] == required_data
        assert payload['fromDate'] == from_date
        assert payload['toDate'] == to_date
        assert payload['interval'] == 1  # Default value

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_expired_options_data_invalid_interval(self, mock_create_request, dhanhq_obj):
        json_response = dhanhq_obj.expired_options_data(
            "13", "NSE_FNO", "OPTIDX", "MONTH", 1, "ATM", "CALL", 
            ["open"], "2023-01-01", "2023-01-31", interval=10
        )
        assert json_response['status'] == 'failure'
        assert "interval value must be" in json_response['remarks']
        mock_create_request.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_expired_options_data_invalid_expiry_flag(self, mock_create_request, dhanhq_obj):
        json_response = dhanhq_obj.expired_options_data(
            "13", "NSE_FNO", "OPTIDX", "YEAR", 1, "ATM", "CALL", 
            ["open"], "2023-01-01", "2023-01-31"
        )
        assert json_response['status'] == 'failure'
        assert "expiry_flag value must be" in json_response['remarks']
        mock_create_request.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_expired_options_data_invalid_option_type(self, mock_create_request, dhanhq_obj):
        json_response = dhanhq_obj.expired_options_data(
            "13", "NSE_FNO", "OPTIDX", "MONTH", 1, "ATM", "BOTH", 
            ["open"], "2023-01-01", "2023-01-31"
        )
        assert json_response['status'] == 'failure'
        assert "drv_option_type value must be" in json_response['remarks']
        mock_create_request.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_expired_options_data_invalid_required_data(self, mock_create_request, dhanhq_obj):
        json_response = dhanhq_obj.expired_options_data(
            "13", "NSE_FNO", "OPTIDX", "MONTH", 1, "ATM", "CALL", 
            ["open", "invalid_field"], "2023-01-01", "2023-01-31"
        )
        assert json_response['status'] == 'failure'
        assert "required_data must only contain" in json_response['remarks']
        mock_create_request.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_intraday_minute_data(self, mock_create_request, dhanhq_obj):
        endpoint = '/charts/intraday'
        security_id = "security_id"
        exchange_segment = "exchange_segment"
        instrument_type = "instrument_type"
        from_date = "from_date"
        to_date = "to_date"
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        
        json_response = dhanhq_obj.intraday_minute_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_intraday_minute_data_fails_for_bad_interval_input(self, mock_create_request, dhanhq_obj):
        security_id = "security_id"
        exchange_segment = "exchange_segment"
        instrument_type = "instrument_type"
        from_date = "from_date"
        to_date = "to_date"
        interval = 100
        
        json_response = dhanhq_obj.intraday_minute_data(security_id, exchange_segment, instrument_type, from_date, to_date, interval)
        
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value
        assert "interval value must be" in json_response['remarks']
        mock_create_request.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_historical_daily_data(self, mock_create_request, dhanhq_obj):
        endpoint = '/charts/historical'
        security_id = 'security_id'
        exchange_segment = 'exchange_segment'
        instrument_type = 'instrument_type'
        from_date = "from_date"
        to_date = "to_date"
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        
        json_response = dhanhq_obj.historical_daily_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_historical_daily_data_fails_for_bad_expiry_code(self, mock_create_request, dhanhq_obj):
        security_id = 'security_id'
        exchange_segment = 'exchange_segment'
        instrument_type = 'instrument_type'
        from_date = "from_date"
        to_date = "to_date"
        bad_expiry_code = 99
        
        json_response = dhanhq_obj.historical_daily_data(security_id, exchange_segment, instrument_type, from_date, to_date, bad_expiry_code)
        
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value
        assert "expiry_code value must be" in json_response['remarks']
        mock_create_request.assert_not_called()
