from unittest.mock import patch
from dhanhq import dhanhq

class TestDhanhq_OptionChain:
    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_option_chain(self, mock_create_request, dhanhq_obj):
        security_id = 13
        exchange_segment = "IDX_I"
        expiry = "2024-10-31"
        dhanhq_obj.option_chain(security_id, exchange_segment, expiry)
        mock_create_request.assert_called_once_with(
            '/optionchain',
            {
                "UnderlyingScrip": security_id,
                "UnderlyingSeg": exchange_segment,
                "Expiry": expiry
            }
        )
