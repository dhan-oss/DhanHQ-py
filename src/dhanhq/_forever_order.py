from dhanhq.constants.exchange_segment import ExchangeSegment
from dhanhq.constants.leg_name import LegName
from dhanhq.constants.order_flag import OrderFlag
from dhanhq.constants.order_type import OrderType
from dhanhq.constants.product_type import ProductType
from dhanhq.constants.transaction_type import TransactionType
from dhanhq.constants.validity import Validity


class ForeverOrder:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def place_forever(self, security_id: str, exchange_segment: ExchangeSegment, transaction_type: TransactionType,
                      product_type: ProductType, order_type: OrderType, quantity: int, price: float,
                      trigger_Price: float, order_flag: OrderFlag=OrderFlag.SINGLE, disclosed_quantity: int=0,
                      validity: Validity=Validity.DAY, price1: float=0, trigger_Price1: float=0, quantity1: int=0,
                      tag: str=None, symbol: str="") -> dict[str,str]:
        """
        Place a new forever order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (ExchangeSegment): The exchange segment (e.g., NSE, BSE).
            transaction_type (TransactionType): The type of transaction (BUY/SELL).
            product_type (ProductType): The product type (e.g., CNC, INTRA).
            order_type (OrderType): The type of order (LIMIT, MARKET, etc.).
            quantity (int): The quantity of the order.
            price (float): The price of the order.
            trigger_Price (float): The trigger price for the order.
            order_flag (OrderFlag): The order flag (default is SINGLE).
            disclosed_quantity (int): The disclosed quantity for the order.
            validity (Validity): The validity of the order (DAY, IOC, etc.).
            price1 (float): The secondary price for the order.
            trigger_Price1 (float): The secondary trigger price for the order.
            quantity1 (int): The secondary quantity for the order.
            tag (str): Optional correlation ID for tracking.
            symbol (str): The trading symbol for the order.

        Returns:
            dict: The response containing the status of the order placement.
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

        return self.dhan_http.post(endpoint, payload)

    def modify_forever(self, order_id: str, order_flag: OrderFlag, order_type: OrderType, leg_name: LegName,
                       quantity: int, price: float, trigger_price: float, disclosed_quantity: int, validity: Validity) -> dict[str, str]:
        """
        Modify a forever order based on the specified leg name.
        The variables that can be modified include price, quantity, order type, and validity.

        Args:
            order_id (str): The ID of the order to modify.
            order_flag (OrderFlag): The order flag indicating the type of order (e.g., SINGLE, OCO).
            order_type (OrderType): The type of order (e.g., LIMIT, MARKET).
            leg_name (LegName): The name of the leg to modify.
            quantity (int): The new quantity for the order.
            price (float): The new price for the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            validity (Validity): The validity of the order.

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
        return self.dhan_http.put(endpoint, payload)

    def get_forever(self):
        """Retrieve a list of all existing Forever Orders."""
        endpoint = '/forever/orders'
        return self.dhan_http.get(endpoint)

    def cancel_forever(self, order_id):
        """Delete Forever orders using the order id of an order."""
        endpoint = f'/forever/orders/{order_id}'
        return self.dhan_http.delete(endpoint)
