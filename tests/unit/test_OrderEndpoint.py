from unittest.mock import patch

from dhanhq.constant import AMOTime, ExchangeSegment, LegName, OrderType, ProductType, TransactionType, Validity


class TestOrderEndpoint:
    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_order_list_success(self, mock_read_request, dhanhq_obj):
        orderEndpoint = dhanhq_obj.orderEndpoint
        orderEndpoint.get_order_list()
        mock_read_request.assert_called_once_with('/orders')

    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_order_by_id(self, mock_read_request, dhanhq_obj):
        orderEndpoint = dhanhq_obj.orderEndpoint
        order_id = "12345"
        orderEndpoint.get_order_by_id(order_id)
        mock_read_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_order_by_correlation_id(self, mock_read_request, dhanhq_obj):
        orderEndpoint = dhanhq_obj.orderEndpoint
        correlation_id = "12345"
        orderEndpoint.get_order_by_correlationID(correlation_id)
        mock_read_request.assert_called_once_with(f'/orders/external/{correlation_id}')

    @patch("dhanhq.http.DhanHTTP.delete")
    def test_cancel_order_success(self, mock_delete_request, dhanhq_obj):
        orderEndpoint = dhanhq_obj.orderEndpoint
        order_id = "12345"
        orderEndpoint.cancel_order(order_id)
        mock_delete_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.http.DhanHTTP.post")
    def test_place_order_success(self,mock_create_request,dhanhq_obj):
        orderEndpoint = dhanhq_obj.orderEndpoint
        endpoint = '/orders'
        security_id = 1
        exchange_segment = ExchangeSegment.NSE_EQ
        transaction_type = TransactionType.BUY
        quantity =100
        order_type = OrderType.MARKET
        product_type = ProductType.CNC
        price = 123
        orderEndpoint.place_order(security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity=Validity.DAY, amo_time=AMOTime.OPEN,
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.post")
    def test_place_slice_order_success(self,mock_create_request,dhanhq_obj):
        orderEndpoint = dhanhq_obj.orderEndpoint
        endpoint = '/orders/slicing'
        security_id = 1
        exchange_segment = ExchangeSegment.NSE_EQ
        transaction_type = TransactionType.BUY
        quantity =100
        order_type = OrderType.MARKET
        product_type = ProductType.CNC
        price = 123
        orderEndpoint.place_slice_order(security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity=Validity.DAY, amo_time=AMOTime.OPEN,
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.put")
    def test_modify_order_success(self,mock_update_request,dhanhq_obj):
        orderEndpoint = dhanhq_obj.orderEndpoint
        order_id = 123
        endpoint = f'/orders/{order_id}'
        quantity = 100
        price = 99
        trigger_price = 100
        orderEndpoint.modify_order(order_id, OrderType.STOP_LOSS, LegName.STOP_LOSS_LEG, quantity, price,
                                trigger_price, trigger_price, Validity.IOC)
        mock_update_request.assert_called_once()
        assert mock_update_request.call_args[0][0] == endpoint
