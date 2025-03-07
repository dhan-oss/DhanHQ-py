
class Order:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_order_list(self):
        """
        Retrieve a list of all orders requested in a day with their last updated status.

        Returns:
            dict: The response containing order list status and data.
        """
        return self.dhan_http.get('/orders')

    def get_order_by_id(self, order_id):
        """
        Retrieve the details and status of an order from the orderbook placed during the day.

        Args:
            order_id (str): The ID of the order to retrieve.

        Returns:
            dict: The response containing order details and status.
        """
        return self.dhan_http.get(f'/orders/{order_id}')

    def get_order_by_correlationID(self, correlation_id):
        """
        Retrieve the order status using a field called correlation_id.

        Args:
            correlation_id (str): The correlation_id provided during order placement.

        Returns:
            dict: The response containing order status.
        """
        return self.dhan_http.get(f'/orders/external/{correlation_id}')

    def modify_order(self, order_id, order_type, leg_name, quantity,
                     price, trigger_price, disclosed_quantity, validity):
        """
        Modify a pending order in the orderbook.

        Args:
            order_id (str): The ID of the order to modify.
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
        payload = {
            "orderId": str(order_id),
            "orderType": order_type,
            "legName": leg_name,
            "quantity": quantity,
            "price": price,
            "disclosedQuantity": disclosed_quantity,
            "triggerPrice": trigger_price,
            "validity": validity
        }
        return self.dhan_http.put(f'/orders/{order_id}', payload)

    def cancel_order(self, order_id):
        """
        Cancel a pending order in the orderbook using the order ID.

        Args:
            order_id (str): The ID of the order to cancel.

        Returns:
            dict: The response containing the status of the cancellation.
        """
        return self.dhan_http.delete(f'/orders/{order_id}')

    def place_order(self, security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity='DAY', amo_time='OPEN',
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None, should_slice=False):
        """
        Place a new order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            transaction_type (str): The type of transaction (BUY/SELL).
            quantity (int): The quantity of the order.
            order_type (str): The type of order (LIMIT, MARKET, etc.).
            product_type (str): The product type (CNC, INTRA, etc.).
            price (float): The price of the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            after_market_order (bool): Flag for after market order.
            validity (str): The validity of the order (DAY, IOC, etc.).
            amo_time (str): The time for AMO orders.
            bo_profit_value (float): The profit value for BO orders.
            bo_stop_loss_Value (float): The stop loss value for BO orders.
            tag (str): Optional correlation ID for tracking.

        Returns:
            dict: The response containing the status of the order placement.
        """

        if after_market_order and (amo_time not in ['OPEN', 'OPEN_30', 'OPEN_60']):
            raise Exception("amo_time value must be one of ['OPEN','OPEN_30','OPEN_60']")

        payload = {
            "transactionType": transaction_type.upper(),
            "exchangeSegment": exchange_segment.upper(),
            "productType": product_type.upper(),
            "orderType": order_type.upper(),
            "validity": validity.upper(),
            "securityId": security_id,
            "quantity": int(quantity),
            "disclosedQuantity": int(disclosed_quantity),
            "price": float(price),
            "afterMarketOrder": after_market_order,
            "boProfitValue": bo_profit_value,
            "boStopLossValue": bo_stop_loss_Value,
            "triggerPrice": float(trigger_price)
        }

        if tag is not None and tag != '':
            payload["correlationId"] = tag

        endpoint = '/orders'
        if should_slice:
            endpoint += '/slicing'
        return self.dhan_http.post(endpoint, payload)

    def place_slice_order(self, security_id, exchange_segment, transaction_type, quantity,
                          order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                          after_market_order=False, validity='DAY', amo_time='OPEN',
                          bo_profit_value=None, bo_stop_loss_Value=None, tag=None):
        """
        Place a new slice order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            transaction_type (str): The type of transaction (BUY/SELL).
            quantity (int): The quantity of the order.
            order_type (str): The type of order (LIMIT, MARKET, etc.).
            product_type (str): The product type (CNC, MIS, etc.).
            price (float): The price of the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            after_market_order (bool): Flag for after market order.
            validity (str): The validity of the order (DAY, IOC, etc.).
            amo_time (str): The time for AMO orders.
            bo_profit_value (float): The profit value for BO orders.
            bo_stop_loss_Value (float): The stop loss value for BO orders.
            tag (str): Optional correlation ID for tracking.

        Returns:
            dict: The response containing the status of the slice order placement.
        """

        return self.place_order(security_id, exchange_segment, transaction_type, quantity,
                                order_type, product_type, price, trigger_price, disclosed_quantity,
                                after_market_order, validity, amo_time,
                                bo_profit_value, bo_stop_loss_Value, tag, True)
