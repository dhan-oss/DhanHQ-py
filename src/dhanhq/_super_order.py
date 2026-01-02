class SuperOrder:
    """
    Interface to manage Dhan 'Super Orders', which are composite trading orders that include
    multiple legs: ENTRY_LEG, TARGET_LEG, and STOP_LOSS_LEG.

    These allow users to define entry, target, and stop-loss instructions as a bundled strategy.
    """

    def __init__(self, dhan_context):
        """
        Initialize SuperOrder with Dhan HTTP context.
        """
        self.dhan_http = dhan_context.get_dhan_http()

    def get_super_order_list(self):
        """
        Retrieve a list of all live/requested super orders with their latest status.

        Returns:
            dict: The API response containing the list of super orders and their status.
        """
        return self.dhan_http.get('/super/orders')

    def modify_super_order(self, order_id, order_type, leg_name, quantity=0,
                           price=0.0, targetPrice=0.0, stopLossPrice=0.0, trailingJump=0.0):
        """
        Modify a pending super order leg.

        Super orders consist of three possible legs: ENTRY_LEG, TARGET_LEG, STOP_LOSS_LEG.
        Based on the leg_name provided, this modifies only the respective leg parameters.

        Args:
            order_id (str): ID of the order to modify (required).
            order_type (str): Order type (e.g., LIMIT, MARKET).
            leg_name (str): Must be one of ENTRY_LEG, TARGET_LEG, STOP_LOSS_LEG.
            quantity (int): Updated quantity (for ENTRY_LEG).
            price (float): Updated price (for ENTRY_LEG).
            targetPrice (float): Target price (for ENTRY_LEG or TARGET_LEG).
            stopLossPrice (float): Stop loss price (for ENTRY_LEG or STOP_LOSS_LEG).
            trailingJump (float): Trailing jump trigger (for ENTRY_LEG or STOP_LOSS_LEG).

        Returns:
            dict: The API response with update status.

        Raises:
            ValueError: If leg_name or order_id is missing or invalid.
        """
        if not order_id:
            raise ValueError("Order ID must be provided.")
        if leg_name not in ("ENTRY_LEG", "TARGET_LEG", "STOP_LOSS_LEG"):
            raise ValueError(f"Invalid leg_name: {leg_name}. Must be one of ENTRY_LEG, TARGET_LEG, STOP_LOSS_LEG.")

        payload = None
        match str(leg_name).upper():
            case "ENTRY_LEG":
                payload = {
                    "orderId": str(order_id),
                    "orderType": order_type,
                    "legName": "ENTRY_LEG",
                    "quantity": int(quantity),
                    "price": float(price),
                    "targetPrice": float(targetPrice),
                    "stopLossPrice": float(stopLossPrice),
                    "trailingJump": float(trailingJump)
                }
            case "TARGET_LEG":
                payload = {
                    "orderId": str(order_id),
                    "legName": "TARGET_LEG",
                    "targetPrice": float(targetPrice)
                }
            case "STOP_LOSS_LEG":
                payload = {
                    "orderId": str(order_id),
                    "legName": "STOP_LOSS_LEG",
                    "stopLossPrice": float(stopLossPrice),
                    "trailingJump": float(trailingJump)
                }
            case _:
                raise ValueError(f"Invalid leg_name: {leg_name}. Expected: ENTRY_LEG, TARGET_LEG, or STOP_LOSS_LEG")

        return self.dhan_http.put(f'/super/orders/{order_id}', payload)

    def cancel_super_order(self, order_id, order_leg):
        """
        Cancel a super order or a specific leg.

        Cancelling the main order ID cancels all legs. If a target or stop-loss leg is cancelled individually,
        it cannot be added again later.

        Args:
            order_id (str): The ID of the order to cancel (required).
            order_leg (str): The leg to cancel: ENTRY_LEG, TARGET_LEG, or STOP_LOSS_LEG.

        Returns:
            dict: API response indicating cancellation status.

        Raises:
            ValueError: If parameters are missing or invalid.
        """
        if not order_id:
            raise ValueError("Order ID must be provided.")
        if order_leg not in ("ENTRY_LEG", "TARGET_LEG", "STOP_LOSS_LEG"):
            raise ValueError("Invalid order_leg provided.")

        return self.dhan_http.delete(f'/super/orders/{order_id}/{order_leg}')

    def place_super_order(self, security_id, exchange_segment, transaction_type, quantity,
                      order_type, product_type, price, targetPrice=0.0, stopLossPrice=0.0,
                      trailingJump=0.0, tag=None):
        """
        Place a new Super Order on Dhan platform with entry, target and stop-loss legs.

        Args:
            security_id (str): Instrument/security ID (required).
            exchange_segment (str): Exchange (e.g., NSE, BSE).
            transaction_type (str): BUY or SELL.
            quantity (int): Order quantity (> 0).
            order_type (str): LIMIT, MARKET, etc.
            product_type (str): CNC, INTRA, etc.
            price (float): Entry price.
            targetPrice (float): Target price.
            stopLossPrice (float): Stop loss price.
            trailingJump (float): Trailing SL value.
            tag (str): Optional correlation ID or tracking label.

        Returns:
            dict: The response containing the order placement status.

        Raises:
            ValueError: If mandatory inputs are missing or logically invalid.
        """
        # Basic validations
        if not all([security_id, exchange_segment, transaction_type, quantity, order_type, product_type, price]):
            raise ValueError("Missing required parameters for placing a super order.")

        # Leg validation
        if price <= 0:
            raise ValueError("Price must be > 0.")

        if targetPrice <= 0 and stopLossPrice <= 0:
            raise ValueError("At least one of targetPrice or stopLossPrice must be provided and > 0.")

        transaction_type = transaction_type.upper()
        price = float(price)
        targetPrice = float(targetPrice)
        stopLossPrice = float(stopLossPrice)

        # Logical leg validation
        if transaction_type == "BUY":
            if targetPrice > 0 and not (targetPrice > price):
                raise ValueError("For BUY: targetPrice must be > price.")
            if stopLossPrice > 0 and not (stopLossPrice < price):
                raise ValueError("For BUY: stopLossPrice must be < price.")
        elif transaction_type == "SELL":
            if targetPrice > 0 and not (targetPrice < price):
                raise ValueError("For SELL: targetPrice must be < price.")
            if stopLossPrice > 0 and not (stopLossPrice > price):
                raise ValueError("For SELL: stopLossPrice must be > price.")
        else:
            raise ValueError("transaction_type must be either BUY or SELL.")

        payload = {
            "transactionType": transaction_type,
            "exchangeSegment": exchange_segment.upper(),
            "productType": product_type.upper(),
            "orderType": order_type.upper(),
            "securityId": security_id,
            "quantity": int(quantity),
            "price": price,
            "targetPrice": float(targetPrice),
            "stopLossPrice": float(stopLossPrice),
            "trailingJump": float(trailingJump)
        }

        if tag:
            payload["correlationId"] = tag
    
        endpoint = '/super/orders'

        return self.dhan_http.post(endpoint, payload)

