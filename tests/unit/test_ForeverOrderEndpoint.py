from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, LegName, OrderFlag, OrderType, ProductType, TransactionType, Validity
from dhanhq.dto import NewForeverOrderRequest, ModifyForeverOrderRequest


class TestForeverOrderEndpoint:
    @staticmethod
    def __order_stub():
        return {
            "dhanClientId": "1000000132",
            "correlationId": "",
            "orderFlag": "OCO",
            "transactionType": "BUY",
            "exchangeSegment": "NSE_EQ",
            "productType": "CNC",
            "orderType": "LIMIT",
            "validity": "DAY",
            "securityId": "1333",
            "quantity": 5,
            "disclosedQuantity": 1,
            "price": 1428,
            "triggerPrice": 1427,
            "price1": 1420,
            "triggerPrice1": 1419,
            "quantity1": 10
        }

    @staticmethod
    def __list_of_orders_stub():
        return [
            {
                "dhanClientId": "1000000132",
                "orderId": "1132208051115",
                "orderStatus": "CONFIRM",
                "transactionType": "BUY",
                "exchangeSegment": "NSE_EQ",
                "productType": "CNC",
                "orderFlag": "SINGLE",
                "tradingSymbol": "HDFCBANK",
                "securityId": "1333",
                "quantity": 10,
                "price": 1428,
                "triggerPrice": 1427,
                "legName": "ENTRY_LEG",
                "createTime": "2022-08-05 12:41:19",
                "updateTime": "",
                "exchangeTime": "",
                "drvExpiryDate": "",
                "drvOptionType": "",
                "drvStrikePrice": 0
            }
        ]


    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_forever_orders(self,mock_read_request,dhanhq_obj):
        mock_read_request.return_value = self.__list_of_orders_stub()
        dhanhq_obj.foreverOrderEndpoint.get_forever_orders()
        mock_read_request.assert_called_once_with('/forever/orders')

    @patch("dhanhq.http.DhanHTTP.post")
    def test_place_forever_order(self,mock_create_request, dhanhq_obj):
        mock_create_request.return_value = { "orderId": "112111182045", "orderStatus": "PENDING" }
        endpoint = '/forever/orders'
        requestParams = NewForeverOrderRequest(security_id="1",
                                        exchange_segment=ExchangeSegment.NSE_EQ,
                                        transaction_type=TransactionType.BUY,
                                        quantity=100,
                                        order_type=OrderType.MARKET,
                                        product_type=ProductType.CNC,
                                        price=123,
                                        trigger_price=110)
        dhanhq_obj.foreverOrderEndpoint.place_forever_order(requestParams)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.put")
    def test_modify_forever_order(self, mock_update_request, dhanhq_obj):
        mock_update_request.return_value = { "orderId": "123", "orderStatus": "PENDING" }
        requestParams = ModifyForeverOrderRequest(order_id="123",
                                                  order_flag=OrderFlag.SINGLE,
                                                  order_type=OrderType.STOP_LOSS,
                                                  leg_name=LegName.STOP_LOSS_LEG,
                                                  quantity=100,
                                                  price=108,
                                                  trigger_price=110,
                                                  disclosed_quantity=555,
                                                  validity=Validity.IOC)
        endpoint = f'/forever/orders/{requestParams.order_id}'
        dhanhq_obj.foreverOrderEndpoint.modify_forever_order(requestParams)
        mock_update_request.assert_called_once()
        assert mock_update_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.delete")
    def test_cancel_forever_order(self, mock_delete_request, dhanhq_obj):
        mock_delete_request.return_value = { "orderId": "112111182045", "orderStatus": "CANCELLED" }
        order_id = "123"
        endpoint = f'/forever/orders/{order_id}'
        dhanhq_obj.foreverOrderEndpoint.cancel_pending_forever_order(order_id)
        mock_delete_request.assert_called_once_with(endpoint)
