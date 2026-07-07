from unittest.mock import patch


class TestDhanhq_ConditionalOrder:
    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_conditional_order(self, mock_post_request, dhanhq_obj):
        endpoint = '/alerts/orders'
        condition = {
            "comparisonType": "PRICE_WITH_VALUE",
            "exchangeSegment": "NSE_EQ",
            "securityId": "1333",
            "operator": "GREATER_THAN",
            "comparingValue": 250,
            "frequency": "ONCE"
        }
        orders = [{
            "transactionType": "BUY",
            "exchangeSegment": "NSE_EQ",
            "productType": "CNC",
            "orderType": "LIMIT",
            "securityId": "1333",
            "quantity": 10,
            "validity": "DAY",
            "price": "250.00"
        }]
        dhanhq_obj.place_conditional_order(condition, orders)
        mock_post_request.assert_called_once()
        assert mock_post_request.call_args[0][0] == endpoint
        payload = mock_post_request.call_args[0][1]
        assert payload["condition"] == condition
        assert payload["orders"] == orders

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_conditional_orders(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_conditional_orders()
        mock_get_request.assert_called_once_with('/alerts/orders')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_conditional_order(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_conditional_order("12345")
        mock_get_request.assert_called_once_with('/alerts/orders/12345')

    @patch("dhanhq.dhan_http.DhanHTTP.put")
    def test_modify_conditional_order(self, mock_put_request, dhanhq_obj):
        condition = {"comparisonType": "PRICE_WITH_VALUE", "securityId": "1333"}
        dhanhq_obj.modify_conditional_order("12345", condition)
        mock_put_request.assert_called_once()
        assert mock_put_request.call_args[0][0] == '/alerts/orders/12345'
        payload = mock_put_request.call_args[0][1]
        assert payload["alertId"] == "12345"
        assert payload["condition"] == condition

    @patch("dhanhq.dhan_http.DhanHTTP.delete")
    def test_cancel_conditional_order(self, mock_delete_request, dhanhq_obj):
        dhanhq_obj.cancel_conditional_order("12345")
        mock_delete_request.assert_called_once_with('/alerts/orders/12345')
