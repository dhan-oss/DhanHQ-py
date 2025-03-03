from dhanhq.constant import ExchangeSegment, ProductType, TransactionType
from dhanhq.dto import Margin
from dhanhq.dto.compute_margin_request import ComputeMarginRequest


class FundsEndpoint:

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

    def compute_margin_info(self, margin_req: ComputeMarginRequest) -> Margin:
        """
        Calculate the margin required for a trade based on the provided parameters.
        """
        endpoint = '/margincalculator'
        payload = {
            "securityId": margin_req.security_id,
            "exchangeSegment": margin_req.exchange_segment.name,
            "transactionType": margin_req.transaction_type.name,
            "quantity": margin_req.quantity,
            "productType": margin_req.product_type.name,
            "price": margin_req.price
        }
        # ToDo: Shouldn't price and trigger_price being float vlaues be rounded to 2 or 3 decimal places as precision??
        if margin_req.trigger_price >= 0:
            payload["triggerPrice"] = margin_req.trigger_price

        dict_response = self.dhan_http.post(endpoint, payload)
        return Margin(**dict_response)
