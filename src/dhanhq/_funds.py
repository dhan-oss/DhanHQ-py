from dhanhq.constants.exchange_segment import ExchangeSegment
from dhanhq.constants.product_type import ProductType
from dhanhq.constants.transaction_type import TransactionType


class Funds:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_fund_limits(self):
        """
        Get all information of your trading account like balance, margin utilized, collateral, etc.

        Returns:
            dict: The response containing fund limits data.
        """
        endpoint = '/fundlimit'
        return self.dhan_http.get(endpoint)

    def margin_calculator(self, security_id: str, exchange_segment: ExchangeSegment, transaction_type: TransactionType,
                          quantity: int, product_type: ProductType, price: float, trigger_price: float=0) -> dict[str, str]:
        """
        Calculate the margin required for a trade based on the provided parameters.

        Args:
            security_id (str): The ID of the security for which the margin is to be calculated.
            exchange_segment (ExchangeSegment): The exchange segment (e.g., NSE_EQ) where the trade will be executed.
            transaction_type (TransactionType): The type of transaction (BUY/SELL).
            quantity (int): The quantity of the security to be traded.
            product_type (ProductType): The product type (e.g., CNC, INTRA) of the trade.
            price (float): The price at which the trade will be executed.
            trigger_price (float, optional): The trigger price for the trade. Defaults to 0.

        Returns:
            dict: The response containing the margin calculation result.
        """
        endpoint = '/margincalculator'
        payload = {
            "securityId": security_id,
            "exchangeSegment": exchange_segment.name,
            "transactionType": transaction_type.name,
            "quantity": int(quantity),
            "productType": product_type.name,
            "price": float(price)
        }
        # ToDo: Shouldn't price and trigger_price being float vlaues be rounded to 2 or 3 decimal places as precision??
        if trigger_price >= 0:
            payload["triggerPrice"] = float(trigger_price)

        return self.dhan_http.post(endpoint, payload)
