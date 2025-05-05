
class SuperOrder:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_super_order_list(self):
        """
        Retrieve a list of all super orders requested in a day with their last updated status.

        Returns:
            dict: The response containing order list status and data.
        """
        return self.dhan_http.get('/super/orders')

    def modify_super_order(self, order_id, order_type, leg_name, quantity=0,
                     price=0.0, targetPrice=0.0, stopLossPrice=0.0, trailingJump=0.0):
        """
        Modify a pending order in the orderbook.

        Args:
            order_id (str): The ID of the order to modify.
            order_type (str): The type of order (e.g., LIMIT, MARKET).
            leg_name (str): The name of the leg to modify.
            quantity (int): The new quantity for the order.
            price (float): The new price for the order.
            targetPrice (float): The target price for the order.
            stopLossPrice (float): The stop loss price for the order.
            trailingJump (float): The trailing jump price of the order.

        Returns:
            dict: The response containing the status of the modification.
        """
        match str(leg_name).upper():
            case "ENTRY_LEG":
                payload = {
                    "orderId": str(order_id),
                    "orderType": order_type,
                    "legName": str(leg_name).upper(),
                    "quantity": int(quantity),
                    "price": float(price),
                    "targetPrice": float(targetPrice),
                    "stopLossPrice": float(stopLossPrice),
                    "trailingJump": float(trailingJump)
                }
            case "TARGET_LEG":
                payload = {
                    "orderId": str(order_id),
                    "legName": str(leg_name).upper(),
                    "targetPrice": float(targetPrice),
                }
            case "STOP_LOSS_LEG":
                payload = {
                    "orderId": str(order_id),
                    "legName": str(leg_name).upper(),
                    "stopLossPrice": float(stopLossPrice),
                    "trailingJump": float(trailingJump)
                } 
        return self.dhan_http.put(f'/super/orders/{order_id}', payload)

    def cancel_super_order(self, order_id, order_leg):
        """
        Cancel a pending order in the orderbook using the order ID.

        Args:
            order_id (str): The ID of the order to cancel.
            order_leg (str): The order Leg ENTRY_LEG, TARGET_LEG, STOP_LOSS_LEG

        Note:   Cancelling main order ID cancels all legs. If particular target or
                stop loss leg is cancelled, then the same cannot be added again.

        Returns:
            dict: The response containing the status of the cancellation.
        """
        return self.dhan_http.delete(f'/super/orders/{order_id}/{order_leg}')

    def place_super_order(self, security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, targetPrice, stopLossPrice,
                    trailingJump, tag):
        """
        Place a new super order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            transaction_type (str): The type of transaction (BUY/SELL).
            quantity (int): The quantity of the order.
            order_type (str): The type of order (LIMIT, MARKET, etc.).
            product_type (str): The product type (CNC, INTRA, etc.).
            price (float): The price of the order.
            targetPrice (float): The target profit price for orders.
            stopLossPrice (float): The stop loss price for orders.
            trailingJump (float): The trailing jump point for orders.
            tag (str): Optional correlation ID for tracking.

        Returns:
            dict: The response containing the status of the order placement.
        """

        payload = {
            "transactionType": transaction_type.upper(),
            "exchangeSegment": exchange_segment.upper(),
            "productType": product_type.upper(),
            "orderType": order_type.upper(),
            "securityId": security_id,
            "quantity": int(quantity),
            "price": float(price),
            "targetPrice": float(targetPrice),
            "stopLossPrice": float(stopLossPrice),
            "trailingJump": float(trailingJump)
        }

        if tag is not None and tag != '':
            payload["correlationId"] = tag

        endpoint = '/super/orders'
        return self.dhan_http.post(endpoint, payload)
