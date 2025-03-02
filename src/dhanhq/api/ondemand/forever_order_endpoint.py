from typing import Optional, List

from pydantic import TypeAdapter

from dhanhq.constant import ExchangeSegment, LegName, OrderFlag, OrderType, ProductType, TransactionType, Validity
from dhanhq.dto import ForeverOrderResponse, ForeverOrder


class ForeverOrderEndpoint:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def place_forever_order(self, security_id: str, exchange_segment: ExchangeSegment, transaction_type: TransactionType,
                            product_type: ProductType, order_type: OrderType, quantity: int, price: float,
                            trigger_Price: float, order_flag: OrderFlag=OrderFlag.SINGLE, disclosed_quantity: int=0,
                            validity: Validity=Validity.DAY, price1: float=0, trigger_Price1: float=0, quantity1: int=0,
                            tag: Optional[str]=None, symbol: str="") -> ForeverOrderResponse:
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
            "orderFlag": order_flag.name,
            "transactionType": transaction_type.name,
            "exchangeSegment": exchange_segment.name,
            "productType": product_type.name,
            "orderType": order_type.name,
            "validity": validity.name,
            "tradingSymbol": symbol,
            "securityId": security_id,
            "quantity": int(quantity),
            "disclosedQuantity": int(disclosed_quantity),
            "price": float(price),
            "triggerPrice": float(trigger_Price),
            "price1": float(price1),
            "triggerPrice1": float(trigger_Price1),
            "quantity1": int(quantity1),
        }

        if tag not in (None, ''):
            payload["correlationId"] = tag

        dict_response = self.dhan_http.post(endpoint, payload)
        return ForeverOrderResponse(**dict_response)

    def modify_forever_order(self, order_id: str, order_flag: OrderFlag, order_type: OrderType, leg_name: LegName,
                             quantity: int, price: float, trigger_price: float, disclosed_quantity: int, validity: Validity) -> ForeverOrderResponse:
        """
        Modify a forever order_req based on the specified leg name.
        The variables that can be modified include price, quantity, order_req type, and validity.

        Args:
            order_id (str): The ID of the order_req to modify.
            order_flag (OrderFlag): The order_req flag indicating the type of order_req (e.g., SINGLE, OCO).
            order_type (OrderType): The type of order_req (e.g., LIMIT, MARKET).
            leg_name (LegName): The name of the leg to modify.
            quantity (int): The new quantity for the order_req.
            price (float): The new price for the order_req.
            trigger_price (float): The trigger price for the order_req.
            disclosed_quantity (int): The disclosed quantity for the order_req.
            validity (Validity): The validity of the order_req.

        Returns:
            dict: The response containing the status of the modification.
        """
        endpoint = f'/forever/orders/{order_id}'
        payload = {
            "orderId": str(order_id),
            "orderFlag": order_flag.name,
            "orderType": order_type.name,
            "legName": leg_name.name,
            "quantity": quantity,
            "disclosedQuantity": disclosed_quantity,
            "price": price,
            "triggerPrice": trigger_price,
            "validity": validity.name
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
