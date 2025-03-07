
class OptionChain:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def option_chain(self, under_security_id, under_exchange_segment, expiry):
        """
        Retrieve the real-time Option Chain for a specified underlying instrument.

        Args:
            under_security_id (int): The security ID of the underlying instrument.
            under_exchange_segment (str): The exchange segment of the underlying instrument (e.g., NSE, BSE).
            expiry (str): The expiry date of the options.

        Returns:
            dict: The response containing Open Interest (OI), Greeks, Volume, Last Traded Price,
                    Best Bid/Ask, and Implied Volatility (IV) across all strikes for the specified underlying.
        """
        endpoint = '/optionchain'
        payload = {
            "UnderlyingScrip": under_security_id,
            "UnderlyingSeg": under_exchange_segment,
            "Expiry": expiry
        }
        return self.dhan_http.post(endpoint, payload)

    def expiry_list(self, under_security_id, under_exchange_segment):
        """
        Retrieve the dates of all expiries for a specified underlying instrument.

        Args:
            under_security_id (int): The security ID of the underlying instrument.
            under_exchange_segment (str): The exchange segment of the underlying instrument (e.g., NSE, BSE).

        Returns:
            dict: The response containing list of dates for which option expiries
                    are present for the specified underlying instrument.
        """
        endpoint = '/optionchain/expirylist'
        payload = {
            "UnderlyingScrip": under_security_id,
            "UnderlyingSeg": under_exchange_segment
        }
        return self.dhan_http.post(endpoint, payload)

