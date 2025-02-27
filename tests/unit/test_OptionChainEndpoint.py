from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, InstrumentType
from dhanhq.http import DhanHTTP

class TestOptionChainEndpoint:

    @patch("dhanhq.http.DhanHTTP.post")
    def test_option_chain(self, mock_create_request, dhanhq_obj):
        optionChainEndpoint = dhanhq_obj.optionChainEndpoint
        endpoint = '/optionchain'
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = optionChainEndpoint.option_chain("under_security_id", "under_exchange_segment", "expiry")
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.post")
    def test_expiry_list(self, mock_create_request, dhanhq_obj):
        optionChainEndpoint = dhanhq_obj.optionChainEndpoint
        endpoint = '/optionchain/expirylist'
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = optionChainEndpoint.expiry_list("under_security_id", ExchangeSegment.NSE_FNO)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
