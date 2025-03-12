"""
This API gives you historical candle data for the desired scrip across segments & exchange.
This data is presented in the form of a candle and gives you timestamp, open, high, low, close (OHLC) & volume.
"""
import logging

class HistoricalData:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def intraday_minute_data(self, security_id, exchange_segment, instrument_type, from_date, to_date, interval=1):
        """
        Retrieve OHLC & Volume of minute candles for desired instrument for last 5 trading day.

        Args:
            security_id (str): The ID of the security.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            instrument_type (str): The type of instrument (e.g., stock, option).

        Returns:
            dict: The response containing intraday minute data.
        """
        if interval not in [1, 5, 15, 25, 60]:
            # Raising and catching an exception in same method is bad practice. Replaced it with this clean code
            err = "interval value must be ['1','5','15','25','60']"
            logging.error('Exception in dhanhq>>intraday_minute_data: %s', err)
            return {
                'status': 'failure',
                'remarks': err,
                'data': '',
            }
        endpoint = '/charts/intraday'
        payload = {
            'securityId': security_id,
            'exchangeSegment': exchange_segment,
            'instrument': instrument_type,
            'interval': interval,
            'fromDate': from_date,
            'toDate': to_date
        }
        return self.dhan_http.post(endpoint, payload)

    def historical_daily_data(self, security_id, exchange_segment, instrument_type, from_date, to_date, expiry_code=0):
        """
        Retrieve OHLC & Volume of daily candle for desired instrument.

        Args:
            security_id (str): Security ID of the instrument.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            instrument_type (str): The type of instrument (e.g., stock, option).
            expiry_code (str): The expiry code for derivatives.
            from_date (str): The start date for the historical data.
            to_date (str): The end date for the historical data.

        Returns:
            dict: The response containing historical daily data.
        """
        if expiry_code not in [0, 1, 2, 3]:
            err = "expiry_code value must be ['0','1','2','3']"
            logging.error('Exception in dhanhq>>historical_daily_data: %s', err)
            return {
                'status': 'failure',
                'remarks': err,
                'data': '',
            }
        endpoint = '/charts/historical'
        payload = {
            "securityId": security_id,
            "exchangeSegment": exchange_segment,
            "instrument": instrument_type,
            "expiryCode": expiry_code,
            "fromDate": from_date,
            "toDate": to_date
        }
        return self.dhan_http.post(endpoint, payload)
