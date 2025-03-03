from typing import Optional, List

from pydantic import TypeAdapter

from dhanhq.constant import ExchangeSegment, LegName, OrderFlag, OrderType, ProductType, TransactionType, Validity
from dhanhq.dto import ForeverOrderResponse, ForeverOrder, ModifyForeverOrderRequest, NewForeverOrderRequest


class ForeverOrderEndpoint:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def place_forever_order(self, feo_req: NewForeverOrderRequest) -> ForeverOrderResponse:
        """
        Place a new forever order_req in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (ExchangeSegment): The exchange segment (e.g., NSE, BSE).
            transaction_type (TransactionType): The type of transaction (BUY/SELL).
            product_type (ProductType): The product type (e.g., CNC, INTRA).
            order_type (OrderType): The type of order_req (LIMIT, MARKET, etc.).
            quantity (int): The quantity of the order_req.
            price (float): The price of the order_req.
            trigger_Price (float): The trigger price for the order_req.
            order_flag (OrderFlag): The order_req flag (default is SINGLE).
            disclosed_quantity (int): The disclosed quantity for the order_req.
            validity (Validity): The validity of the order_req (DAY, IOC, etc.) defaults to DAY.
            price1 (float): The secondary price for the order_req.
            trigger_Price1 (float): The secondary trigger price for the order_req.
            quantity1 (int): The secondary quantity for the order_req.
            tag (Optional[str]): Optional correlation ID for tracking.
            symbol (str): The trading symbol for the order_req.

        Returns:
            dict: The response containing the status of the order_req placement.
        """
        endpoint = '/forever/orders'
        payload = {
            "orderFlag": feo_req.order_flag.name,
            "transactionType": feo_req.transaction_type.name,
            "exchangeSegment": feo_req.exchange_segment.name,
            "productType": feo_req.product_type.name,
            "orderType": feo_req.order_type.name,
            "validity": feo_req.validity.name,
            "securityId": feo_req.security_id,
            "quantity": feo_req.quantity,
            "disclosedQuantity": feo_req.disclosed_quantity,
            "price": feo_req.price,
            "triggerPrice": feo_req.trigger_price,
            "price1": feo_req.price1,
            "triggerPrice1": feo_req.trigger_price1,
            "quantity1": feo_req.quantity1,
        }

        if feo_req.correlation_id not in (None, ''):
            payload["correlationId"] = feo_req.correlation_id

        dict_response = self.dhan_http.post(endpoint, payload)
        return ForeverOrderResponse(**dict_response)

    def modify_forever_order(self, feo_req: ModifyForeverOrderRequest) -> ForeverOrderResponse:
        """
        Modify a forever order_req based on the specified leg name.
        The variables that can be modified include price, quantity, order_req type, and validity.
        """
        endpoint = f'/forever/orders/{feo_req.order_id}'
        payload = {
            "orderId": feo_req.order_id,
            "orderFlag": feo_req.order_flag.name,
            "orderType": feo_req.order_type.name,
            "legName": feo_req.leg_name.name,
            "quantity": feo_req.quantity,
            "disclosedQuantity": feo_req.disclosed_quantity,
            "price": feo_req.price,
            "triggerPrice": feo_req.trigger_price,
            "validity": feo_req.validity.name
        }
        dict_response = self.dhan_http.put(endpoint, payload)
        return ForeverOrderResponse(**dict_response)

    def get_forever_orders(self) -> list[ForeverOrder]:
        """Retrieve a list of all existing Forever Orders."""
        endpoint = '/forever/orders'
        dict_response = self.dhan_http.get(endpoint)
        adapter = TypeAdapter(List[ForeverOrder])
        forever_orders = adapter.validate_python(dict_response)
        return forever_orders

    def cancel_pending_forever_order(self, order_id) -> ForeverOrderResponse:
        """Delete Forever orders using the order_req id of an order_req."""
        endpoint = f'/forever/orders/{order_id}'
        dict_response = self.dhan_http.delete(endpoint)
        return ForeverOrderResponse(**dict_response)
