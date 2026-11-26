
class ConditionalOrder:
    """Conditional (alert-based) orders and multi order placement - the /alerts/ endpoints."""

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def place_conditional_order(self, condition, orders):
        """
        Create a conditional order (alert) that places one or more orders automatically
        when the given price/technical-indicator condition is met.

        Args:
            condition (dict): The trigger condition. Keys (camelCase):
                comparisonType (TECHNICAL_WITH_VALUE / TECHNICAL_WITH_INDICATOR /
                    TECHNICAL_WITH_CLOSE / PRICE_WITH_VALUE),
                exchangeSegment (NSE_EQ / BSE_EQ / IDX_I), securityId,
                indicatorName (e.g. SMA_20, EMA_50, RSI_14, MACD_HIST - passed as string),
                timeFrame (DAY / ONE_MIN / FIVE_MIN / FIFTEEN_MIN),
                operator (CROSSING_UP / CROSSING_DOWN / CROSSING_ANY_SIDE / GREATER_THAN /
                    LESS_THAN / GREATER_THAN_EQUAL / LESS_THAN_EQUAL / EQUAL / NOT_EQUAL),
                comparingValue, comparingIndicatorName, expDate (default 1 year),
                frequency (ONCE / ALWAYS), userNote.
                Conditions are supported only for Equities and Indices.
            orders (list): List of order dicts to place when triggered. Each order keys:
                transactionType, exchangeSegment, productType (CNC / INTRADAY / MARGIN / MTF),
                orderType (LIMIT / MARKET / STOP_LOSS / STOP_LOSS_MARKET), securityId,
                quantity, validity (DAY / IOC), price, discQuantity, triggerPrice.

        Returns:
            dict: The response containing the created conditional order details.
        """
        payload = {
            "condition": condition,
            "orders": orders
        }
        return self.dhan_http.post('/alerts/orders', payload)

    def place_multi_order(self, orders):
        """
        Place multiple orders in a single request, directly and without any condition.

        Args:
            orders (list): List of order dicts to place, up to 15 per request.
                Orders are placed in the sequence given. Each order keys (camelCase):
                sequence (required, str): Sequence number to identify order in the batch,
                    starting with 1 for the first order,
                correlationId (str, up to 30 characters): The user/partner generated id
                    for tracking back,
                transactionType (required, BUY / SELL),
                exchangeSegment (required, NSE_EQ / NSE_FNO / NSE_COMM / BSE_EQ /
                    BSE_FNO / MCX_COMM),
                productType (CNC / INTRADAY / MARGIN / MTF),
                orderType (LIMIT / MARKET / STOP_LOSS / STOP_LOSS_MARKET),
                validity (DAY / IOC), securityId, quantity,
                afterMarketOrder (bool), amoTime (OPEN / OPEN_30 / OPEN_60 / PRE_OPEN),
                price, triggerPrice, disclosedQuantity.

        Returns:
            dict: The response containing the list of order responses, each holding
                orderId, sequence and orderStatus (TRANSIT / PENDING / REJECTED /
                CANCELLED / PART_TRADED / TRADED / EXPIRED / MODIFIED / TRIGGERED /
                INACTIVE).

        Raises:
            ValueError: If no orders are given. The 15 order cap is enforced by the
                API itself, which reports the received and allowed counts.
        """
        if not orders:
            raise ValueError("At least one order must be provided.")

        payload = {
            "orders": orders
        }
        return self.dhan_http.post('/alerts/multi/orders', payload)

    def get_conditional_orders(self):
        """
        Retrieve all conditional orders (alerts) for the authenticated account.

        Returns:
            dict: The response containing the list of conditional orders.
        """
        return self.dhan_http.get('/alerts/orders')

    def get_conditional_order(self, alert_id):
        """
        Retrieve the status and details of a specific conditional order.

        Args:
            alert_id (str): The unique identifier of the conditional order.

        Returns:
            dict: The response containing the conditional order details.
        """
        return self.dhan_http.get(f'/alerts/orders/{alert_id}')

    def modify_conditional_order(self, alert_id, condition, orders=None):
        """
        Modify a conditional order's condition and/or associated orders.

        Args:
            alert_id (str): The unique identifier of the conditional order to modify.
            condition (dict): The updated trigger condition (see place_conditional_order).
            orders (list, optional): The updated list of orders. Defaults to None.

        Returns:
            dict: The response containing the status of the modification.
        """
        payload = {
            "alertId": str(alert_id),
            "condition": condition
        }
        if orders is not None:
            payload["orders"] = orders
        return self.dhan_http.put(f'/alerts/orders/{alert_id}', payload)

    def cancel_conditional_order(self, alert_id):
        """
        Delete an existing conditional order.

        Args:
            alert_id (str): The unique identifier of the conditional order to delete.

        Returns:
            dict: The response containing the status of the deletion.
        """
        return self.dhan_http.delete(f'/alerts/orders/{alert_id}')
