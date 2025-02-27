from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, LegName, OrderFlag, OrderType, ProductType, TransactionType, Validity


class TestForeverOrderEndpoint:
    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_forever(self,mock_read_request,dhanhq_obj):
        foreverOrderEndpoint = dhanhq_obj.foreverOrderEndpoint
        foreverOrderEndpoint.get_forever()
        mock_read_request.assert_called_once_with('/forever/orders')

    @patch("dhanhq.http.DhanHTTP.post")
    def test_place_forever(self,mock_create_request, dhanhq_obj):
        foreverOrderEndpoint = dhanhq_obj.foreverOrderEndpoint
        endpoint = '/forever/orders'
        quantity = 100
        price = 108
        trigger_Price = 110
        foreverOrderEndpoint.place_forever("security_id", ExchangeSegment.BSE_EQ, TransactionType.BUY,
                                 ProductType.INTRADAY, OrderType.STOP_LOSS, quantity, price, trigger_Price)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.put")
    def test_modify_forever(self, mock_update_request, dhanhq_obj):
        foreverOrderEndpoint = dhanhq_obj.foreverOrderEndpoint
        order_id = 123
        endpoint = f'/forever/orders/{order_id}'
        quantity = 100
        price = 108
        trigger_price = 110
        disclosed_quantity = 555
        foreverOrderEndpoint.modify_forever(order_id, OrderFlag.SINGLE, OrderType.STOP_LOSS, LegName.STOP_LOSS_LEG,
                                  quantity, price, trigger_price, disclosed_quantity,Validity.IOC)
        mock_update_request.assert_called_once()
        assert mock_update_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.delete")
    def test_cancel_forever(self, mock_delete_request, dhanhq_obj):
        foreverOrderEndpoint = dhanhq_obj.foreverOrderEndpoint
        order_id = "123"
        endpoint = f'/forever/orders/{order_id}'
        foreverOrderEndpoint.cancel_forever(order_id)
        mock_delete_request.assert_called_once_with(endpoint)
