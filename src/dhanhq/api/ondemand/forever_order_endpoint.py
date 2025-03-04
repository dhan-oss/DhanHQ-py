from typing import Optional, List, Union

from pydantic import TypeAdapter

from dhanhq.constant import ExchangeSegment, LegName, OrderFlag, OrderType, ProductType, TransactionType, Validity
from dhanhq.dto import ForeverOrderResponse, ForeverOrder, ModifyForeverOrderRequest, NewForeverOrderRequest
from dhanhq.http import DhanAPIException


class ForeverOrderEndpoint:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def place_forever_order(self, feo_req: NewForeverOrderRequest) -> ForeverOrderResponse:
        """
        Place a new forever order_req in the Dhan account.
        """
        endpoint = '/forever/orders'
        dict_response = self.dhan_http.post(endpoint, feo_req.model_dump())
        return ForeverOrderResponse(**dict_response)

    def modify_forever_order(self, feo_req: ModifyForeverOrderRequest) -> ForeverOrderResponse:
        """
        Modify a forever order_req based on the specified leg name.
        The variables that can be modified include price, quantity, order_req type, and validity.
        """
        endpoint = f'/forever/orders/{feo_req.order_id}'
        dict_response = self.dhan_http.put(endpoint, feo_req.model_dump())
        return ForeverOrderResponse(**dict_response)

    def get_forever_orders(self) -> list[ForeverOrder]:
        """Retrieve a list of all existing Forever Orders."""
        endpoint = '/forever/orders'
        list_response = self.dhan_http.get(endpoint)
        adapter = TypeAdapter(List[ForeverOrder])
        forever_orders = adapter.validate_python(list_response)
        return forever_orders

    def cancel_pending_forever_order(self, order_id) -> ForeverOrderResponse:
        """Delete Forever orders using the order_req id of an order_req."""
        endpoint = f'/forever/orders/{order_id}'
        dict_response = self.dhan_http.delete(endpoint)
        return ForeverOrderResponse(**dict_response)
