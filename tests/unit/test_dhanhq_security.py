from unittest.mock import patch
from dhanhq import dhanhq

class TestDhanhq_Security:
    @patch("requests.get")
    @patch("builtins.open", new_callable=lambda: patch("builtins.open").start())
    @patch("pandas.read_csv")
    def test_fetch_security_list(self, mock_read_csv, mock_open, mock_requests_get, dhanhq_obj):
        mock_requests_get.return_value.content = b"header,header\nval,val"
        dhanhq_obj.fetch_security_list()
        mock_requests_get.assert_called_once_with('https://images.dhan.co/api-data/api-scrip-master.csv')

    @patch("requests.get")
    @patch("builtins.open", new_callable=lambda: patch("builtins.open").start())
    @patch("pandas.read_csv")
    def test_fetch_security_list_compact(self, mock_read_csv, mock_open, mock_requests_get, dhanhq_obj):
        mock_requests_get.return_value.content = b"header,header\nval,val"
        dhanhq_obj.fetch_security_list("compact")
        mock_requests_get.assert_called_once_with('https://images.dhan.co/api-data/api-scrip-master.csv')

    @patch("requests.get")
    @patch("builtins.open", new_callable=lambda: patch("builtins.open").start())
    @patch("pandas.read_csv")
    def test_fetch_segment_security_list(self, mock_read_csv, mock_open, mock_requests_get, dhanhq_obj):
        mock_requests_get.return_value.content = b"header,header\nval,val"
        result = dhanhq_obj.fetch_segment_security_list("NSE_EQ")
        mock_requests_get.assert_called_once_with('https://api.dhan.co/v2/instrument/NSE_EQ')
        mock_open.assert_called_once_with('security_id_list_NSE_EQ.csv', 'wb')
        assert result is mock_read_csv.return_value

    @patch("requests.get")
    @patch("builtins.open", new_callable=lambda: patch("builtins.open").start())
    @patch("pandas.read_csv")
    def test_fetch_segment_security_list_custom_filename(self, mock_read_csv, mock_open, mock_requests_get,
                                                         dhanhq_obj):
        mock_requests_get.return_value.content = b"header,header\nval,val"
        dhanhq_obj.fetch_segment_security_list("MCX_COMM", filename="mcx.csv")
        mock_requests_get.assert_called_once_with('https://api.dhan.co/v2/instrument/MCX_COMM')
        mock_open.assert_called_once_with('mcx.csv', 'wb')

    @patch("requests.get")
    @patch("pandas.read_csv")
    def test_fetch_segment_security_list_invalid_segment(self, mock_read_csv, mock_requests_get, dhanhq_obj):
        import requests
        mock_requests_get.return_value.raise_for_status.side_effect = requests.HTTPError("404 Client Error")
        assert dhanhq_obj.fetch_segment_security_list("FOO") is None
        mock_read_csv.assert_not_called()
