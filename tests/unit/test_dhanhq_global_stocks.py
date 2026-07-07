from unittest.mock import patch


class TestDhanhq_GlobalStocks:
    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_global_order(self, mock_post_request, dhanhq_obj):
        dhanhq_obj.place_global_order("AAPL_ID", "BUY", "LIMIT", quantity=5, price=150.5)
        mock_post_request.assert_called_once()
        assert mock_post_request.call_args[0][0] == '/globalstocks/orders'
        payload = mock_post_request.call_args[0][1]
        assert payload["transactionType"] == "BUY"
        assert payload["orderType"] == "LIMIT"
        assert payload["securityId"] == "AAPL_ID"
        assert payload["quantity"] == 5.0
        assert payload["price"] == 150.5

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_global_order_list(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_global_order_list()
        mock_get_request.assert_called_once_with('/globalstocks/orders')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_global_order_by_id(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_global_order_by_id("111")
        mock_get_request.assert_called_once_with('/globalstocks/orders/111')

    @patch("dhanhq.dhan_http.DhanHTTP.put")
    def test_modify_global_order(self, mock_put_request, dhanhq_obj):
        dhanhq_obj.modify_global_order("111", "LIMIT", "BUY", "AAPL_ID", quantity=3, price=149.0,
                                       leg_name="ENTRY_LEG")
        mock_put_request.assert_called_once()
        assert mock_put_request.call_args[0][0] == '/globalstocks/orders/111'
        payload = mock_put_request.call_args[0][1]
        assert payload["legName"] == "ENTRY_LEG"
        assert payload["quantity"] == 3.0

    @patch("dhanhq.dhan_http.DhanHTTP.delete")
    def test_cancel_global_order(self, mock_delete_request, dhanhq_obj):
        dhanhq_obj.cancel_global_order("111")
        mock_delete_request.assert_called_once_with('/globalstocks/orders/111')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_global_trades(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_global_trades()
        mock_get_request.assert_called_once_with('/globalstocks/trades')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_global_trades_by_security(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_global_trades_by_security("AAPL_ID")
        mock_get_request.assert_called_once_with('/globalstocks/trades/AAPL_ID')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_global_holdings(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_global_holdings()
        mock_get_request.assert_called_once_with('/globalstocks/holdings')

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_global_trans_estimate(self, mock_post_request, dhanhq_obj):
        dhanhq_obj.global_trans_estimate("AAPL_ID", "150", "5", "BUY")
        mock_post_request.assert_called_once()
        assert mock_post_request.call_args[0][0] == '/globalstocks/transEstimate'
        payload = mock_post_request.call_args[0][1]
        assert payload == {"securityId": "AAPL_ID", "price": "150", "quantity": "5", "transactionType": "BUY"}

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_global_margin_calculator(self, mock_post_request, dhanhq_obj):
        dhanhq_obj.global_margin_calculator("AAPL_ID", "150", "5", "BUY")
        mock_post_request.assert_called_once()
        assert mock_post_request.call_args[0][0] == '/globalstocks/margincalculator'

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_global_market_status(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_global_market_status()
        mock_get_request.assert_called_once_with('/globalstocks/marketstatus')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_global_fund_limit(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_global_fund_limit()
        mock_get_request.assert_called_once_with('/globalstocks/fundlimit')
