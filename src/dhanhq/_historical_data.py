"""
This API gives you historical candle data for the desired scrip across segments & exchange.
This data is presented in the form of a candle and gives you timestamp, open, high, low, close (OHLC) & volume.
"""
import logging

class HistoricalData:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def intraday_minute_data(self, security_id, exchange_segment, instrument_type, from_date, to_date, interval=1, oi=False):
        """
        Retrieve OHLC & Volume of minute candles for desired instrument for last 5 trading day.

        Args:
            security_id (str): The ID of the security.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            instrument_type (str): The type of instrument (e.g., stock, option).
            from_date (str): The start date for the historical data (YYYY-MM-DD).
            to_date (str): The end date for the historical data (YYYY-MM-DD).
            interval (int): Time interval - 1, 5, 15, 25, or 60 minutes (default: 1).
            oi (bool): Fetch Open Interest data (default: False).

        Returns:
            dict: The response containing intraday minute data.
        """

        endpoint = '/charts/intraday'
        payload = {
            'securityId': security_id,
            'exchangeSegment': exchange_segment,
            'instrument': instrument_type,
            'interval': interval,
            'oi': oi,
            'fromDate': from_date,
            'toDate': to_date
        }
        return self.dhan_http.post(endpoint, payload)

    def historical_daily_data(self, security_id, exchange_segment, instrument_type, from_date, to_date, expiry_code=0, oi=False):
        """
        Retrieve OHLC & Volume of daily candle for desired instrument.

        Args:
            security_id (str): Security ID of the instrument.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            instrument_type (str): The type of instrument (e.g., stock, option).
            from_date (str): The start date for the historical data (YYYY-MM-DD).
            to_date (str): The end date for the historical data (YYYY-MM-DD).
            expiry_code (int): The expiry code for derivatives (0, 1, 2, 3).
            oi (bool): Fetch Open Interest data (default: False).

        Returns:
            dict: The response containing historical daily data.
        """
        if expiry_code not in [0, 1, 2, 3]:
            err = "expiry_code value must be [0, 1, 2, 3]"
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
            "oi": oi,
            "fromDate": from_date,
            "toDate": to_date
        }
        return self.dhan_http.post(endpoint, payload)

    def expired_options_data(self, security_id, exchange_segment, instrument_type, expiry_flag, expiry_code, strike, drv_option_type, required_data, from_date, to_date, interval=1):
        """
        Fetch expired options data on a rolling basis.

        Args:
            security_id (str): Security ID of the underlying instrument.
            exchange_segment (str): Exchange segment (e.g., NSE_FNO).
            instrument_type (str): Instrument type (e.g., OPTIDX, OPTSTK).
            expiry_flag (str): Expiry flag - 'WEEK' or 'MONTH'.
            expiry_code (int): Expiry code (0, 1, 2, 3).
            strike (str): Strike price relative to spot (e.g., ATM, ATM+1, ATM-1).
            drv_option_type (str): Option type - 'CALL' or 'PUT'.
            required_data (list): List of data fields to fetch (open, high, low, close, iv, volume, strike, oi, spot).
            from_date (str): Start date (YYYY-MM-DD format).
            to_date (str): End date (YYYY-MM-DD format).
            interval (int): Time interval - 1, 5, 15, 25, or 60 minutes (default: 1).

        Returns:
            dict: The response containing expired options data.
        """
        if interval not in [1, 5, 15, 25, 60]:
            err = "interval value must be [1, 5, 15, 25, 60]"
            logging.error('Exception in dhanhq>>expired_options_data: %s', err)
            return {
                'status': 'failure',
                'remarks': err,
                'data': '',
            }
        
        if expiry_flag not in ["WEEK", "MONTH"]:
            err = "expiry_flag value must be ['WEEK', 'MONTH']"
            logging.error('Exception in dhanhq>>expired_options_data: %s', err)
            return {
                'status': 'failure',
                'remarks': err,
                'data': '',
            }
            
        if drv_option_type not in ["CALL", "PUT"]:
            err = "drv_option_type value must be ['CALL', 'PUT']"
            logging.error('Exception in dhanhq>>expired_options_data: %s', err)
            return {
                'status': 'failure',
                'remarks': err,
                'data': '',
            }
            
        valid_fields = ["open", "high", "low", "close", "iv", "volume", "strike", "oi", "spot"]
        if not all(field in valid_fields for field in required_data):
            err = f"required_data must only contain {valid_fields}"
            logging.error('Exception in dhanhq>>expired_options_data: %s', err)
            return {
                'status': 'failure',
                'remarks': err,
                'data': '',
            }

        endpoint = '/charts/rollingoption'
        payload = {
            "securityId": security_id,
            "exchangeSegment": exchange_segment,
            "instrument": instrument_type,
            "expiryFlag": expiry_flag,
            "expiryCode": expiry_code,
            "strike": strike,
            "drvOptionType": drv_option_type,
            "requiredData": required_data,
            "fromDate": from_date,
            "toDate": to_date,
            "interval": interval
        }
        return self.dhan_http.post(endpoint, payload)


