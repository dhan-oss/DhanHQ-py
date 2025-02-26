"""
This API gives you historical candle data for the desired scrip across segments & exchange.
This data is presented in the form of a candle and gives you timestamp, open, high, low, close (OHLC) & volume.
"""
import logging

from dhanhq.constants import ExchangeSegment, ExpiryCode, InstrumentType, Interval


class HistoricalData:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def intraday_minute_data(self, security_id: str, exchange_segment: ExchangeSegment,
                             instrument_type: InstrumentType, from_date:str, to_date: str, interval: Interval=Interval.ONE_MINUTE) -> dict[str, str]:
        """
        Retrieve OHLC & Volume of minute candles for desired instrument for last 5 trading day.

        Args:
            security_id (str): The ID of the security.
            exchange_segment (ExchangeSegment): The exchange segment (e.g., NSE, BSE).
            instrument_type (InstrumentType): The type of instrument (e.g., stock, option).
            from_date (str): from data
            to_date (str): to date
            interval (Interval): Defaults to 1 minute interval.

        Returns:
            dict: The response containing intraday minute data.
        """
        endpoint = '/charts/intraday'
        payload = {
            'securityId': security_id,
            'exchangeSegment': exchange_segment.name,
            'instrument': instrument_type.name,
            'interval': interval.value,
            'fromDate': from_date,
            'toDate': to_date
        }
        return self.dhan_http.post(endpoint, payload)

    def historical_daily_data(self, security_id: str, exchange_segment: ExchangeSegment,
                              instrument_type: InstrumentType, from_date: str, to_date: str,
                              expiry_code: ExpiryCode=ExpiryCode.CURRENT_OR_NEAR_EXPIRY):
        """
        Retrieve OHLC & Volume of daily candle for desired instrument.

        Args:
            security_id (str): Security ID of the instrument.
            exchange_segment (ExchangeSegment): The exchange segment (e.g., NSE, BSE).
            instrument_type (InstrumentType): The type of instrument (e.g., stock, option).
            expiry_code (ExpiryCode): The expiry code for derivatives, the default value being CURRENT_OR_NEAR_EXPIRY.
            from_date (str): The start date for the historical data.
            to_date (str): The end date for the historical data.

        Returns:
            dict: The response containing historical daily data.
        """
        endpoint = '/charts/historical'
        payload = {
            "securityId": security_id,
            "exchangeSegment": exchange_segment.name,
            "instrument": instrument_type.name,
            "expiryCode": expiry_code.value,
            "fromDate": from_date,
            "toDate": to_date
        }
        return self.dhan_http.post(endpoint, payload)
