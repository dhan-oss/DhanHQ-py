

class ForeverOrder:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def place_forever(self, security_id, exchange_segment, transaction_type, product_type, order_type,
                      quantity, price, trigger_Price, order_flag="SINGLE", disclosed_quantity=0, validity='DAY',
                      price1=0, trigger_Price1=0, quantity1=0, tag=None, symbol=""):
        """
        Place a new forever order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            transaction_type (str): The type of transaction (BUY/SELL).
            product_type (str): The product type (e.g., CNC, INTRA).
            order_type (str): The type of order (LIMIT, MARKET, etc.).
            quantity (int): The quantity of the order.
            price (float): The price of the order.
            trigger_Price (float): The trigger price for the order.
            order_flag (str): The order flag (default is "SINGLE").
            disclosed_quantity (int): The disclosed quantity for the order.
            validity (str): The validity of the order (DAY, IOC, etc.).
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
            "orderFlag": order_flag,
            "transactionType": transaction_type.upper(),
            "exchangeSegment": exchange_segment.upper(),
            "productType": product_type.upper(),
            "orderType": order_type.upper(),
            "validity": validity.upper(),
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

    def modify_forever(self, order_id, order_flag, order_type, leg_name,
                       quantity, price, trigger_price, disclosed_quantity, validity):
        """
        Modify a forever order based on the specified leg name.
        The variables that can be modified include price, quantity, order type, and validity.

        Args:
            order_id (str): The ID of the order to modify.
            order_flag (str): The order flag indicating the type of order (e.g., SINGLE, OCO).
            order_type (str): The type of order (e.g., LIMIT, MARKET).
            leg_name (str): The name of the leg to modify.
            quantity (int): The new quantity for the order.
            price (float): The new price for the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            validity (str): The validity of the order.

        Returns:
            dict: The response containing the status of the modification.
        """
        endpoint = f'/forever/orders/{order_id}'
        payload = {
            "orderId": str(order_id),
            "orderFlag": order_flag,
            "orderType": order_type,
            "legName": leg_name,
            "quantity": quantity,
            "disclosedQuantity": disclosed_quantity,
            "price": price,
            "triggerPrice": trigger_price,
            "validity": validity
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
