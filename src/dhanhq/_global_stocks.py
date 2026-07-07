
class GlobalStocks:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def place_global_order(self, security_id, transaction_type, order_type, quantity=0,
                           price=0, trigger_price=None, stop_loss_price=None, target_price=None,
                           amount=None, after_market_order=False, tag=None):
        """
        Place a buy or sell order for a US (global) stock.

        Args:
            security_id (str): The exchange standard ID for the scrip.
            transaction_type (str): The type of transaction (BUY/SELL).
            order_type (str): MARKET, LIMIT, STOP_LOSS, STOP_LOSS_MARKET or AMOUNT.
            quantity (float): The quantity of the order. Defaults to 0.
            price (float): Order price in USD. Use 0 for market orders. Defaults to 0.
            trigger_price (float, optional): Price in USD at which order is triggered (stop loss).
            stop_loss_price (float, optional): Stop loss price in USD.
            target_price (float, optional): Target price in USD.
            amount (float, optional): Amount in USD (for AMOUNT order type).
            after_market_order (bool): Flag for after market order. Defaults to False.
            tag (str, optional): User/partner generated id for tracking back (max 30 chars).

        Returns:
            dict: The response containing the status of the order placement.
        """
        payload = {
            "transactionType": transaction_type.upper(),
            "orderType": order_type.upper(),
            "securityId": security_id,
            "quantity": float(quantity),
            "price": float(price),
            "afterMarketOrder": after_market_order
        }
        if trigger_price is not None:
            payload["triggerPrice"] = float(trigger_price)
        if stop_loss_price is not None:
            payload["stopLossPrice"] = float(stop_loss_price)
        if target_price is not None:
            payload["targetPrice"] = float(target_price)
        if amount is not None:
            payload["amount"] = float(amount)
        if tag is not None and tag != '':
            payload["correlationId"] = tag
        return self.dhan_http.post('/globalstocks/orders', payload)

    def get_global_order_list(self):
        """
        Retrieve the current trading day's US stock order book.

        Returns:
            dict: The response containing the list of global stock orders.
        """
        return self.dhan_http.get('/globalstocks/orders')

    def get_global_order_by_id(self, order_id):
        """
        Retrieve the latest details and status for a specific US stock order.

        Args:
            order_id (str): The ID of the order to retrieve.

        Returns:
            dict: The response containing the order details.
        """
        return self.dhan_http.get(f'/globalstocks/orders/{order_id}')

    def modify_global_order(self, order_id, order_type, transaction_type, security_id,
                            quantity=None, price=None, leg_name=None):
        """
        Modify an existing pending US stock order.

        Args:
            order_id (str): The ID of the order to modify.
            order_type (str): MARKET, LIMIT, STOP_LOSS, STOP_LOSS_MARKET or AMOUNT.
            transaction_type (str): The type of transaction (BUY/SELL).
            security_id (str): The exchange standard ID for the scrip.
            quantity (float, optional): The new quantity for the order.
            price (float, optional): Order price in USD. Use 0 for market orders.
            leg_name (str, optional): Leg to modify - ENTRY_LEG, STOP_LOSS_LEG, TARGET_LEG or NA.

        Returns:
            dict: The response containing the status of the modification.
        """
        payload = {
            "orderType": order_type.upper(),
            "transactionType": transaction_type.upper(),
            "securityId": security_id
        }
        if quantity is not None:
            payload["quantity"] = float(quantity)
        if price is not None:
            payload["price"] = float(price)
        if leg_name is not None:
            payload["legName"] = leg_name.upper()
        return self.dhan_http.put(f'/globalstocks/orders/{order_id}', payload)

    def cancel_global_order(self, order_id):
        """
        Cancel an existing pending US stock order.

        Args:
            order_id (str): The ID of the order to cancel.

        Returns:
            dict: The response containing the status of the cancellation.
        """
        return self.dhan_http.delete(f'/globalstocks/orders/{order_id}')

    def get_global_trades(self):
        """
        Retrieve the current trading day's executed US stock trades.

        Returns:
            dict: The response containing the list of trades.
        """
        return self.dhan_http.get('/globalstocks/trades')

    def get_global_trades_by_security(self, security_id):
        """
        Retrieve executed US stock trades filtered by a specific security ID.

        Args:
            security_id (str): The security ID to filter trades by.

        Returns:
            dict: The response containing the list of trades for the security.
        """
        return self.dhan_http.get(f'/globalstocks/trades/{security_id}')

    def get_global_holdings(self):
        """
        Retrieve the authenticated user's current US stock holdings.

        Returns:
            dict: The response containing the list of holdings.
        """
        return self.dhan_http.get('/globalstocks/holdings')

    def global_trans_estimate(self, security_id, price, quantity, transaction_type):
        """
        Estimate the applicable charges for a US stock order before submitting it.

        Args:
            security_id (str): The exchange standard ID for the scrip.
            price (str): Order price in USD. Use 0 for market orders.
            quantity (str): The quantity of the order.
            transaction_type (str): The type of transaction (BUY/SELL).

        Returns:
            dict: The response containing the transaction charge estimate.
        """
        payload = {
            "securityId": str(security_id),
            "price": str(price),
            "quantity": str(quantity),
            "transactionType": transaction_type.upper()
        }
        return self.dhan_http.post('/globalstocks/transEstimate', payload)

    def global_margin_calculator(self, security_id, price, quantity, transaction_type):
        """
        Calculate the margin required for a US stock order before submitting it.

        Args:
            security_id (str): The exchange standard ID for the scrip.
            price (str): Order price in USD. Use 0 for market orders.
            quantity (str): The quantity of the order.
            transaction_type (str): The type of transaction (BUY/SELL).

        Returns:
            dict: The response containing the margin calculation result.
        """
        payload = {
            "securityId": str(security_id),
            "price": str(price),
            "quantity": str(quantity),
            "transactionType": transaction_type.upper()
        }
        return self.dhan_http.post('/globalstocks/margincalculator', payload)

    def get_global_market_status(self):
        """
        Retrieve the current trading status and session timing for the US stock market.

        Returns:
            dict: The response containing the market status.
        """
        return self.dhan_http.get('/globalstocks/marketstatus')

    def get_global_fund_limit(self):
        """
        Retrieve the authenticated user's fund limit details for US stock trading.

        Returns:
            dict: The response containing the fund limit details.
        """
        return self.dhan_http.get('/globalstocks/fundlimit')
