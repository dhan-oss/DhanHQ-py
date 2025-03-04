from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, InstrumentType
from dhanhq.http import DhanHTTP

class TestOptionChainEndpoint:

    @patch("dhanhq.http.DhanHTTP.post")
    def test_option_chain(self, mock_create_request, dhanhq_obj):
        endpoint = '/optionchain'
        mock_create_request.return_value = {
            "last_price": 12345.67,
            "oc": {
                "25000.000000": {
                    "ce": {
                        "last_price": 125.05,
                        "oi": 5962675,
                        "volume": 84202625
                    }
                }
            }
        }

        json_response = dhanhq_obj.optionChainEndpoint.option_chain("under_sec_id", "under_ex_seg", "expiry")
        mock_create_request.assert_called_once()
        assert json_response['last_price'] == 12345.67
        assert mock_create_request.call_args[0][0] == endpoint


    @patch("dhanhq.http.DhanHTTP.post")
    def test_expiry_list(self, mock_create_request, dhanhq_obj):
        endpoint = '/optionchain/expirylist'
        expected_response = [ "2024-10-17", "2024-10-24", "2024-10-31" ]
        mock_create_request.return_value = expected_response
        response = dhanhq_obj.optionChainEndpoint.expiry_list("under_security_id", ExchangeSegment.NSE_FNO)
        mock_create_request.assert_called_once()
        assert response == expected_response
        assert mock_create_request.call_args[0][0] == endpoint
