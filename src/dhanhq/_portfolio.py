
class Portfolio:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_holdings(self):
        """
        Retrieve all holdings bought/sold in previous trading sessions.

        Returns:
            dict: The response containing holdings data.
        """
        return self.dhan_http.get('/holdings')

    def get_positions(self):
        """
        Retrieve a list of all open positions for the day.

        Returns:
            dict: The response containing open positions.
        """
        return self.dhan_http.get('/positions')

    def convert_position(self, from_product_type, exchange_segment, position_type,
                         security_id, convert_qty, to_product_type):
        """
        Convert Position from Intraday to Delivery or vice versa.

        Args:
            from_product_type (str): The product type to convert from (e.g., CNC).
            exchange_segment (str): The exchange segment (e.g., NSE_EQ).
            position_type (str): The type of position (e.g., LONG).
            security_id (str): The ID of the security to convert.
            convert_qty (int): The quantity to convert.
            to_product_type (str): The product type to convert to (e.g., CNC).

        Returns:
            dict: The response containing the status of the conversion.
        """
        endpoint = '/positions/convert'
        payload = {
            "fromProductType": from_product_type,
            "exchangeSegment": exchange_segment,
            "positionType": position_type,
            "securityId": security_id,
            "convertQty": convert_qty,
            "toProductType": to_product_type
        }
        return self.dhan_http.post(endpoint, payload)

