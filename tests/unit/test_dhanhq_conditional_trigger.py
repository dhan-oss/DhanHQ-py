from unittest.mock import patch

from dhanhq import DhanContext
from dhanhq.dhanhq import dhanhq


class TestDhanhq_ConditionalTrigger:
    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_conditional(self, mock_post, dhanhq_obj):
        endpoint = '/alerts/orders'
        dhan_client_id = '12345'
        condition = {"exchangeSegment": "NSE_EQ", "securityId": "1"}
        orders = [{"transactionType": "BUY", "securityId": "1", "quantity": 1, "price": "100"}]

        dhanhq_obj.place_conditional(dhan_client_id, condition, orders)

        mock_post.assert_called_once()
        assert mock_post.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.put")
    def test_modify_conditional(self, mock_put, dhanhq_obj):
        alert_id = 'a1'
        endpoint = f'/alerts/orders/{alert_id}'
        dhan_client_id = '12345'
        condition = {"exchangeSegment": "NSE_EQ", "securityId": "1"}
        orders = [{"transactionType": "BUY", "securityId": "1", "quantity": 1, "price": "100"}]

        dhanhq_obj.modify_conditional(alert_id, dhan_client_id, condition, orders)

        mock_put.assert_called_once()
        assert mock_put.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.delete")
    def test_delete_conditional(self, mock_delete, dhanhq_obj):
        alert_id = 'a1'
        endpoint = f'/alerts/orders/{alert_id}'
        dhanhq_obj.delete_conditional(alert_id)
        mock_delete.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_conditional_by_id(self, mock_get, dhanhq_obj):
        alert_id = 'a1'
        endpoint = f'/alerts/orders/{alert_id}'
        dhanhq_obj.get_conditional_by_id(alert_id)
        mock_get.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_all_conditionals(self, mock_get, dhanhq_obj):
        endpoint = '/alerts/orders'
        dhanhq_obj.get_all_conditionals()
        mock_get.assert_called_once_with(endpoint)
