from typing import List

from pydantic import TypeAdapter

from dhanhq.constant import LegName, OrderType, Validity, OrderStatus
from dhanhq.dto import OrderResponse, NewOrderRequest, ModifyOrderRequest, Order


class OrderEndpoint:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_order_list(self) -> list[Order]:
        """
        Retrieve a list of all orders requested in a day with their last updated status.

        Returns:
            dict: The response containing order_req list status and data.
        """
        dict_response = self.dhan_http.get('/orders')
        adapter = TypeAdapter(List[Order])
        orders = adapter.validate_python(dict_response)
        return orders

    def get_order_by_id(self, order_id: str) -> Order:
        """
        Retrieve the details and status of an order_req from the orderbook placed during the day.

        Args:
            order_id (str): The ID of the order_req to retrieve.

        Returns:
            dict: The response containing order_req details and status.
        """
        dict_response = self.dhan_http.get(f'/orders/{order_id}')
        return Order(**dict_response)

    def get_order_by_correlationID(self, correlation_id: str) -> Order:
        """
        Retrieve the order_req status using a field called correlation_id.

        Args:
            correlation_id (str): The correlation_id provided during order_req placement.

        Returns:
            dict: The response containing order_req status.
        """
        dict_response = self.dhan_http.get(f'/orders/external/{correlation_id}')
        return Order(**dict_response)

    def cancel_pending_order(self, order_id: str) -> OrderResponse:
        """
        Cancel a pending order_req in the orderbook using the order_req ID.

        Args:
            order_id (str): The ID of the order_req to cancel.

        Returns:
            dict: The response containing the status of the cancellation.
        """
        dict_response = self.dhan_http.delete(f'/orders/{order_id}')
        return OrderResponse(**dict_response)

    def place_new_order(self, order_req: NewOrderRequest) -> OrderResponse:
        """
                Place a new slice order_req in the Dhan account.
        """

        payload = {
            "transactionType": order_req.transaction_type.name,
            "exchangeSegment": order_req.exchange_segment.name,
            "productType": order_req.product_type.name,
            "orderType": order_req.order_type.name,
            "validity": order_req.validity.name,
            "securityId": order_req.security_id,
            "quantity": order_req.quantity,
            "disclosedQuantity": order_req.disclosed_quantity,
            "price": order_req.price,
            "afterMarketOrder": order_req.after_market_order,
            "amoTime": order_req.amo_time.name,
            "boProfitValue": order_req.bo_profit_value,
            "boStopLossValue": order_req.bo_stop_loss_Value,
            "triggerPrice": order_req.trigger_price
        }

        if order_req.correlation_id is not None and order_req.correlation_id != '':
            payload["correlationId"] = order_req.correlation_id

        endpoint = '/orders'
        if order_req.should_slice:
            endpoint += '/slicing'

        dict_response = self.dhan_http.post(endpoint, payload)
        return OrderResponse(**dict_response)

    def modify_pending_order(self, order_req: ModifyOrderRequest) -> OrderResponse:
        """
        Modify a pending order_req in the orderbook.
        """
        payload = {
            "orderId": order_req.order_id,
            "orderType": order_req.order_type.name,
            "legName": order_req.leg_name.name,
            "price": order_req.price,
            "quantity": order_req.quantity,
            "disclosedQuantity": order_req.disclosed_quantity,
            "triggerPrice": order_req.trigger_price,
            "validity": order_req.validity.name
        }
        dict_response = self.dhan_http.put(f'/orders/{order_req.order_id}', payload)
        return OrderResponse(**dict_response)

