
class MarketFeed:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def ticker_data(self, securities):
        """
        Retrieve the latest market price for specified instruments.

        Args:
            securities (dict): A dictionary where keys are exchange segments and values are lists of security IDs.
                securities = {
                    "NSE_EQ": [11536],
                    "NSE_FNO": [49081, 49082]
                }

        Returns:
            dict: The response containing last traded price (LTP) data.
        """
        endpoint = '/marketfeed/ltp'
        payload = {exchange_segment: security_id for exchange_segment, security_id in securities.items()}
        return self.dhan_http.post(endpoint, payload)

    def ohlc_data(self, securities):
        """
        Retrieve the Open, High, Low and Close price along with LTP for specified instruments.

        Args:
            securities (dict): A dictionary where keys are exchange segments and values are lists of security IDs.
                securities = {
                    "NSE_EQ": [11536],
                    "NSE_FNO": [49081, 49082]
                }

        Returns:
            dict: The response containing Open, High, Low and Close along with LTP data.
        """
        endpoint = '/marketfeed/ohlc'
        payload = {exchange_segment: security_id for exchange_segment, security_id in securities.items()}
        return self.dhan_http.post(endpoint, payload)

    def quote_data(self, securities):
        """
        Retrieve full details including market depth, OHLC data, OI and volume along with LTP for specified instruments.

        Args:
            securities (dict): A dictionary where keys are exchange segments and values are lists of security IDs.
                securities = {
                    "NSE_EQ": [11536],
                    "NSE_FNO": [49081, 49082]
                }

        Returns:
            dict: The response containing full packet including market depth, last trade,
                    circuit limit, OHLC, OI and volume data.
        """
        endpoint = '/marketfeed/quote'
        payload = {exchange_segment: security_id for exchange_segment, security_id in securities.items()}
        return self.dhan_http.post(endpoint, payload)

