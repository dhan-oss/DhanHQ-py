from typing import Optional

from dhanhq.constant import AMOTime, ExchangeSegment, LegName, OrderType, ProductType, TransactionType, Validity


class OrderEndpoint:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_order_list(self):
        """
        Retrieve a list of all orders requested in a day with their last updated status.

        Returns:
            dict: The response containing order list status and data.
        """
        return self.dhan_http.get('/orders')

    def get_order_by_id(self, order_id: str) -> dict[str, str]:
        """
        Retrieve the details and status of an order from the orderbook placed during the day.

        Args:
            order_id (str): The ID of the order to retrieve.

        Returns:
            dict: The response containing order details and status.
        """
        return self.dhan_http.get(f'/orders/{order_id}')

    def get_order_by_correlationID(self, correlation_id: str) -> dict[str, str]:
        """
        Retrieve the order status using a field called correlation_id.

        Args:
            correlation_id (str): The correlation_id provided during order placement.

        Returns:
            dict: The response containing order status.
        """
        return self.dhan_http.get(f'/orders/external/{correlation_id}')

    def modify_order(self, order_id: str, order_type: OrderType, leg_name: LegName,
                     quantity: int, price: float, trigger_price: float,
                     disclosed_quantity: int, validity: Validity) -> dict[str, str]:
        """
        Modify a pending order in the orderbook.

        Args:
            order_id (str): The ID of the order to modify.
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
        payload = {
            "orderId": str(order_id),
            "orderType": order_type.name,
            "legName": leg_name.name,
            "quantity": quantity,
            "price": price,
            "disclosedQuantity": disclosed_quantity,
            "triggerPrice": trigger_price,
            "validity": validity.name
        }
        return self.dhan_http.put(f'/orders/{order_id}', payload)

    def cancel_order(self, order_id: str):
        """
        Cancel a pending order in the orderbook using the order ID.

        Args:
            order_id (str): The ID of the order to cancel.

        Returns:
            dict: The response containing the status of the cancellation.
        """
        return self.dhan_http.delete(f'/orders/{order_id}')

    def place_order(self, security_id: str, exchange_segment: ExchangeSegment, transaction_type: TransactionType,
                    quantity: int, order_type: OrderType, product_type: ProductType, price: float,
                    trigger_price :float=0, disclosed_quantity: int=0, after_market_order: bool=False,
                    validity: Validity=Validity.DAY, amo_time: AMOTime=AMOTime.OPEN, bo_profit_value: float=0,
                    bo_stop_loss_Value: float=0, tag: Optional[str]=None, should_slice: bool=False) -> dict[str, str]:
        """
        Place a new order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (ExchangeSegment): The exchange segment (e.g., NSE, BSE).
            transaction_type (TransactionType): The type of transaction (BUY/SELL).
            quantity (int): The quantity of the order.
            order_type (OrderType): The type of order (LIMIT, MARKET, etc.).
            product_type (ProductType): The product type (CNC, INTRA, etc.).
            price (float): The price of the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            after_market_order (bool): Flag for after market order.
            validity (Validity): The validity of the order (DAY, IOC, etc.).
            amo_time (AMOTime): The time for AMO orders.
            bo_profit_value (float): The profit value for BO orders.
            bo_stop_loss_Value (float): The stop loss value for BO orders.
            tag (str): Optional correlation ID for tracking.
            should_slice (bool): Defaults to False. Set True to slice order.

        Returns:
            dict: The response containing the status of the order placement.
        """

        payload = {
            "transactionType": transaction_type.name,
            "exchangeSegment": exchange_segment.name,
            "productType": product_type.name,
            "orderType": order_type.name,
            "validity": validity.name,
            "securityId": security_id,
            "quantity": int(quantity),
            "disclosedQuantity": int(disclosed_quantity),
            "price": float(price),
            "afterMarketOrder": after_market_order,
            "amoTime": amo_time.name,
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

    def place_slice_order(self, security_id: str, exchange_segment: ExchangeSegment, transaction_type: TransactionType,
                    quantity: int, order_type: OrderType, product_type: ProductType, price: float,
                    trigger_price :float=0, disclosed_quantity: int=0, after_market_order: bool=False,
                    validity: Validity=Validity.DAY, amo_time: AMOTime=AMOTime.OPEN, bo_profit_value: float=0,
                    bo_stop_loss_Value: float=0, tag: Optional[str]=None) -> dict[str, str]:
        """
        Place a new slice order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (ExchangeSegment): The exchange segment (e.g., NSE, BSE).
            transaction_type (TransactionType): The type of transaction (BUY/SELL).
            quantity (int): The quantity of the order.
            order_type (str): The type of order (LIMIT, MARKET, etc.).
            product_type (ProductType): The product type (CNC, MIS, etc.).
            price (float): The price of the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            after_market_order (bool): Flag for after market order.
            validity (Validity): The validity of the order (DAY, IOC, etc.).
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
