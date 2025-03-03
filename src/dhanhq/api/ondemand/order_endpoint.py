from typing import List

from pydantic import TypeAdapter

from dhanhq.constant import LegName, OrderType, Validity, OrderStatus
from dhanhq.dto import OrderResponse, NewOrderRequest, ModifyOrderRequest, Order


class OrderEndpoint:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_current_orders(self) -> list[Order]:
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

        endpoint = '/orders'
        if order_req.should_slice:
            endpoint += '/slicing'

        dict_response = self.dhan_http.post(endpoint,
                                            order_req.model_dump(exclude={'should_slice'}))
        return OrderResponse(**dict_response)

    def modify_pending_order(self, order_req: ModifyOrderRequest) -> OrderResponse:
        """
        Modify a pending order_req in the orderbook.
        """

        dict_response = self.dhan_http.put(f'/orders/{order_req.order_id}',
                                           order_req.model_dump())
        return OrderResponse(**dict_response)

