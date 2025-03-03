from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, LegName, OrderType, ProductType, TransactionType, Validity
from dhanhq.dto import NewOrderRequest, ModifyOrderRequest


class TestOrderEndpoint:

    @staticmethod
    def __order_stub():
        return {
            "dhanClientId": "1000000003",
            "orderId": "112111182198",
            "correlationId": "123abc678",
            "orderStatus": "PENDING",
            "transactionType": "BUY",
            "exchangeSegment": "NSE_EQ",
            "productType": "INTRADAY",
            "orderType": "MARKET",
            "validity": "DAY",
            "tradingSymbol": "",
            "securityId": "11536",
            "quantity": 5,
            "disclosedQuantity": 0,
            "price": 0.0,
            "triggerPrice": 0.0,
            "afterMarketOrder": False,
            "boProfitValue": 0.0,
            "boStopLossValue": 0.0,
            "legName": "ENTRY_LEG",
            "createTime": "2021-11-24 13:33:03",
            "updateTime": "2021-11-24 13:33:03",
            "exchangeTime": "2021-11-24 13:33:03",
            "drvExpiryDate": "",
            "drvOptionType": "",
            "drvStrikePrice": 0.0,
            "omsErrorCode": "",
            "omsErrorDescription": "",
            "algoId": "string",
            "remainingQuantity": 5,
            "averageTradedPrice": 0,
            "filledQty": 0
        }

    @staticmethod
    def __list_of_orders_stub():
        return [
            {
                "dhanClientId": "1000000009",
                "orderId": "112111182045",
                "exchangeOrderId": "15112111182045",
                "exchangeTradeId": "15112111182045",
                "transactionType": "BUY",
                "exchangeSegment": "NSE_EQ",
                "productType": "INTRADAY",
                "orderType": "LIMIT",
                "tradingSymbol": "TCS",
                "securityId": "11536",
                "tradedQuantity": 40,
                "tradedPrice": 3345.8,
                "createTime": "2021-03-10 11:20:06",
                "updateTime": "2021-11-25 17:35:12",
                "exchangeTime": "2021-11-25 17:35:12",
                "drvExpiryDate": "",
                "drvOptionType": "",
                "drvStrikePrice": 0.0
            }
        ]


    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_orders_success(self, mock_read_request, dhanhq_obj):
        dhanhq_obj.orderEndpoint.get_orders()
        mock_read_request.assert_called_once_with('/orders')

    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_order_by_id(self, mock_read_request, dhanhq_obj):
        mock_read_request.return_value = self.__order_stub()
        order_id = "12345"
        dhanhq_obj.orderEndpoint.get_order_by_id(order_id)
        mock_read_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_order_by_correlation_id(self, mock_read_request, dhanhq_obj):
        mock_read_request.return_value = self.__order_stub()
        correlation_id = "12345"
        order = dhanhq_obj.orderEndpoint.get_order_by_correlationID(correlation_id)
        print(order.model_dump())
        mock_read_request.assert_called_once_with(f'/orders/external/{correlation_id}')

    @patch("dhanhq.http.DhanHTTP.delete")
    def test_cancel_order_success(self, mock_delete_request, dhanhq_obj):
        mock_delete_request.return_value = { "orderId": "112111182045", "orderStatus": "CANCELLED" }
        order_id = "12345"
        dhanhq_obj.orderEndpoint.cancel_pending_order(order_id)
        mock_delete_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.http.DhanHTTP.post")
    def test_place_order_success(self, mock_create_request, dhanhq_obj):
        mock_create_request.return_value = { "orderId": "112111182198", "orderStatus": "PENDING", }
        endpoint = '/orders'
        requestParams = NewOrderRequest(security_id="1",
                                        exchange_segment=ExchangeSegment.NSE_EQ,
                                        transaction_type=TransactionType.BUY,
                                        quantity=100,
                                        order_type=OrderType.MARKET,
                                        product_type=ProductType.CNC,
                                        price=123)
        dhanhq_obj.orderEndpoint.place_new_order(requestParams)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.post")
    def test_place_slice_order_success(self, mock_create_request, dhanhq_obj):
        mock_create_request.return_value = { "orderId": "112111182198", "orderStatus": "PENDING", }
        endpoint = '/orders/slicing'
        requestParams = NewOrderRequest(security_id="1",
                                        exchange_segment=ExchangeSegment.NSE_EQ,
                                        transaction_type=TransactionType.BUY,
                                        quantity=100,
                                        order_type=OrderType.MARKET,
                                        product_type=ProductType.CNC,
                                        price=123,
                                        should_slice=True)
        dhanhq_obj.orderEndpoint.place_new_order(requestParams)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.http.DhanHTTP.put")
    def test_modify_order_success(self, mock_update_request, dhanhq_obj):
        mock_update_request.return_value = { "orderId": "112111182198", "orderStatus": "PENDING", }
        requestParams = ModifyOrderRequest(order_id="123",
                                           quantity=100,
                                           order_type=OrderType.STOP_LOSS,
                                           leg_name=LegName.STOP_LOSS_LEG,
                                           validity=Validity.IOC,
                                           price=99,
                                           trigger_price=100)
        endpoint = f'/orders/{requestParams.order_id}'

        dhanhq_obj.orderEndpoint.modify_pending_order(requestParams)
        mock_update_request.assert_called_once()
        assert mock_update_request.call_args[0][0] == endpoint
