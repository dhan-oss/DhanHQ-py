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
