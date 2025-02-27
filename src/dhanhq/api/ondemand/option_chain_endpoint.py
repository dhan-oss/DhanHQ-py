from dhanhq.constant import ExchangeSegment


class OptionChainEndpoint:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def option_chain(self, under_security_id: int, under_exchange_segment: str, expiry: str) -> dict[str,str]:
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

    def expiry_list(self, under_security_id:int, under_exchange_segment: ExchangeSegment) -> dict[str,str]:
        """
        Retrieve the dates of all expiries for a specified underlying instrument.

        Args:
            under_security_id (int): The security ID of the underlying instrument.
            under_exchange_segment (ExchangeSegment): The exchange segment of the underlying instrument (e.g., NSE_EQ, BSE_FNO).

        Returns:
            dict: The response containing list of dates for which option expiries
                    are present for the specified underlying instrument.
        """
        endpoint = '/optionchain/expirylist'
        payload = {
            "UnderlyingScrip": under_security_id,
            "UnderlyingSeg": under_exchange_segment.name
        }
        return self.dhan_http.post(endpoint, payload)

