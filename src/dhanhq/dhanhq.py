"""
    A class that has core DhanHQ APIs.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2025 by Dhan.
    :license: see LICENSE for details.
"""

import logging
from datetime import datetime, timedelta, timezone
from json import loads as json_loads
from pathlib import Path
from webbrowser import open as web_open

import requests

from dhanhq import DhanHTTP


class dhanhq:
    """DhanHQ Class having Core APIs"""

    """"Constants for HTTP Responses"""
    OTP_SENT = 'OTP sent'

    """Constants for Exchange Segment"""
    NSE = 'NSE_EQ'
    BSE = 'BSE_EQ'
    CUR = 'NSE_CURRENCY'
    MCX = 'MCX_COMM'
    FNO = 'NSE_FNO'
    NSE_FNO = 'NSE_FNO'
    BSE_FNO = 'BSE_FNO'
    INDEX = 'IDX_I'

    """Constants for Transaction Type"""
    BUY = 'BUY'
    SELL = 'SELL'

    """Constants for Product Type"""
    CNC = 'CNC'
    INTRA = "INTRADAY"
    MARGIN = 'MARGIN'
    CO = 'CO'
    BO = 'BO'
    MTF = 'MTF'

    """Constants for Order Type"""
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    SL = "STOP_LOSS"
    SLM = "STOP_LOSS_MARKET"

    """Constants for Validity"""
    DAY = 'DAY'
    IOC = 'IOC'

    """CSV URL for Security ID List"""
    COMPACT_CSV_URL = 'https://images.dhan.co/api-data/api-scrip-master.csv'
    DETAILED_CSV_URL = 'https://images.dhan.co/api-data/api-scrip-master-detailed.csv'

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def _save_as_temp_html_file_and_open_in_browser(self, form_html):
        temp_web_form_html = "temp_form.html"
        with open(temp_web_form_html, "w") as f:
            f.write(form_html)
        web_open(Path.cwd().joinpath(temp_web_form_html).as_uri())

    def get_order_list(self):
        """
        Retrieve a list of all orders requested in a day with their last updated status.

        Returns:
            dict: The response containing order list status and data.
        """
        return self.dhan_http.get('/orders')

    def get_order_by_id(self, order_id):
        """
        Retrieve the details and status of an order from the orderbook placed during the day.

        Args:
            order_id (str): The ID of the order to retrieve.

        Returns:
            dict: The response containing order details and status.
        """
        return self.dhan_http.get(f'/orders/{order_id}')

    def get_order_by_correlationID(self, correlation_id):
        """
        Retrieve the order status using a field called correlation_id.

        Args:
            correlation_id (str): The correlation_id provided during order placement.

        Returns:
            dict: The response containing order status.
        """
        return self.dhan_http.get(f'/orders/external/{correlation_id}')

    def modify_order(self, order_id, order_type, leg_name, quantity,
                     price, trigger_price, disclosed_quantity, validity):
        """
        Modify a pending order in the orderbook.

        Args:
            order_id (str): The ID of the order to modify.
            order_type (str): The type of order (e.g., LIMIT, MARKET).
            leg_name (str): The name of the leg to modify.
            quantity (int): The new quantity for the order.
            price (float): The new price for the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            validity (str): The validity of the order.

        Returns:
            dict: The response containing the status of the modification.
        """
        payload = {
            "orderId": str(order_id),
            "orderType": order_type,
            "legName": leg_name,
            "quantity": quantity,
            "price": price,
            "disclosedQuantity": disclosed_quantity,
            "triggerPrice": trigger_price,
            "validity": validity
        }
        return self.dhan_http.put(f'/orders/{order_id}', payload)

    def cancel_order(self, order_id):
        """
        Cancel a pending order in the orderbook using the order ID.

        Args:
            order_id (str): The ID of the order to cancel.

        Returns:
            dict: The response containing the status of the cancellation.
        """
        return self.dhan_http.delete(f'/orders/{order_id}')

    def place_order(self, security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity='DAY', amo_time='OPEN',
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None):
        """
        Place a new order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            transaction_type (str): The type of transaction (BUY/SELL).
            quantity (int): The quantity of the order.
            order_type (str): The type of order (LIMIT, MARKET, etc.).
            product_type (str): The product type (CNC, INTRA, etc.).
            price (float): The price of the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            after_market_order (bool): Flag for after market order.
            validity (str): The validity of the order (DAY, IOC, etc.).
            amo_time (str): The time for AMO orders.
            bo_profit_value (float): The profit value for BO orders.
            bo_stop_loss_Value (float): The stop loss value for BO orders.
            tag (str): Optional correlation ID for tracking.

        Returns:
            dict: The response containing the status of the order placement.
        """
        payload = {
            "transactionType": transaction_type.upper(),
            "exchangeSegment": exchange_segment.upper(),
            "productType": product_type.upper(),
            "orderType": order_type.upper(),
            "validity": validity.upper(),
            "securityId": security_id,
            "quantity": int(quantity),
            "disclosedQuantity": int(disclosed_quantity),
            "price": float(price),
            "afterMarketOrder": after_market_order,
            "boProfitValue": bo_profit_value,
            "boStopLossValue": bo_stop_loss_Value
        }
        if tag is not None and tag != '':
            payload["correlationId"] = tag
        if after_market_order:
            if amo_time in ['PRE_OPEN', 'OPEN', 'OPEN_30', 'OPEN_60']:
                payload['amoTime'] = amo_time
            else:
                raise Exception("amo_time value must be ['PRE_OPEN','OPEN','OPEN_30','OPEN_60']")
        if trigger_price > 0:
            payload["triggerPrice"] = float(trigger_price)
        elif trigger_price == 0:
            payload["triggerPrice"] = 0.0
        return self.dhan_http.post('/orders', payload)

    def place_slice_order(self, security_id, exchange_segment, transaction_type, quantity,
                          order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                          after_market_order=False, validity='DAY', amo_time='OPEN',
                          bo_profit_value=None, bo_stop_loss_Value=None, tag=None):
        """
        Place a new slice order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            transaction_type (str): The type of transaction (BUY/SELL).
            quantity (int): The quantity of the order.
            order_type (str): The type of order (LIMIT, MARKET, etc.).
            product_type (str): The product type (CNC, MIS, etc.).
            price (float): The price of the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            after_market_order (bool): Flag for after market order.
            validity (str): The validity of the order (DAY, IOC, etc.).
            amo_time (str): The time for AMO orders.
            bo_profit_value (float): The profit value for BO orders.
            bo_stop_loss_Value (float): The stop loss value for BO orders.
            tag (str): Optional correlation ID for tracking.

        Returns:
            dict: The response containing the status of the slice order placement.
        """
        payload = {
            "transactionType": transaction_type.upper(),
            "exchangeSegment": exchange_segment.upper(),
            "productType": product_type.upper(),
            "orderType": order_type.upper(),
            "validity": validity.upper(),
            "securityId": security_id,
            "quantity": int(quantity),
            "disclosedQuantity": int(disclosed_quantity),
            "price": float(price),
            "afterMarketOrder": after_market_order,
            "boProfitValue": bo_profit_value,
            "boStopLossValue": bo_stop_loss_Value
        }
        if tag is not None and tag != '':
            payload["correlationId"] = tag
        if after_market_order:
            if amo_time in ['OPEN', 'OPEN_30', 'OPEN_60']:
                payload['amoTime'] = amo_time
            else:
                raise Exception("amo_time value must be ['OPEN','OPEN_30','OPEN_60']")
        if trigger_price > 0:
            payload["triggerPrice"] = float(trigger_price)
        elif trigger_price == 0:
            payload["triggerPrice"] = 0.0
        return self.dhan_http.post('/orders/slicing', payload)

    def get_positions(self):
        """
        Retrieve a list of all open positions for the day.

        Returns:
            dict: The response containing open positions.
        """
        return self.dhan_http.get('/positions')

    def get_holdings(self):
        """
        Retrieve all holdings bought/sold in previous trading sessions.

        Returns:
            dict: The response containing holdings data.
        """
        return self.dhan_http.get('/holdings')

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

    def place_forever(self, security_id, exchange_segment, transaction_type, product_type, order_type,
                      quantity, price, trigger_Price, order_flag="SINGLE", disclosed_quantity=0, validity='DAY',
                      price1=0, trigger_Price1=0, quantity1=0, tag=None, symbol=""):
        """
        Place a new forever order in the Dhan account.

        Args:
            security_id (str): The ID of the security to trade.
            exchange_segment (str): The exchange segment (e.g., NSE, BSE).
            transaction_type (str): The type of transaction (BUY/SELL).
            product_type (str): The product type (e.g., CNC, INTRA).
            order_type (str): The type of order (LIMIT, MARKET, etc.).
            quantity (int): The quantity of the order.
            price (float): The price of the order.
            trigger_Price (float): The trigger price for the order.
            order_flag (str): The order flag (default is "SINGLE").
            disclosed_quantity (int): The disclosed quantity for the order.
            validity (str): The validity of the order (DAY, IOC, etc.).
            price1 (float): The secondary price for the order.
            trigger_Price1 (float): The secondary trigger price for the order.
            quantity1 (int): The secondary quantity for the order.
            tag (str): Optional correlation ID for tracking.
            symbol (str): The trading symbol for the order.

        Returns:
            dict: The response containing the status of the order placement.
        """
        endpoint = '/forever/orders'
        payload = {
            "orderFlag": order_flag,
            "transactionType": transaction_type.upper(),
            "exchangeSegment": exchange_segment.upper(),
            "productType": product_type.upper(),
            "orderType": order_type.upper(),
            "validity": validity.upper(),
            "tradingSymbol": symbol,
            "securityId": security_id,
            "quantity": int(quantity),
            "disclosedQuantity": int(disclosed_quantity),
            "price": float(price),
            "triggerPrice": float(trigger_Price),
            "price1": float(price1),
            "triggerPrice1": float(trigger_Price1),
            "quantity1": int(quantity1),
        }

        if tag not in (None, ''):
            payload["correlationId"] = tag

        return self.dhan_http.post(endpoint, payload)

    def modify_forever(self, order_id, order_flag, order_type, leg_name,
                       quantity, price, trigger_price, disclosed_quantity, validity):
        """
        Modify a forever order based on the specified leg name.
        The variables that can be modified include price, quantity, order type, and validity.

        Args:
            order_id (str): The ID of the order to modify.
            order_flag (str): The order flag indicating the type of order (e.g., SINGLE, OCO).
            order_type (str): The type of order (e.g., LIMIT, MARKET).
            leg_name (str): The name of the leg to modify.
            quantity (int): The new quantity for the order.
            price (float): The new price for the order.
            trigger_price (float): The trigger price for the order.
            disclosed_quantity (int): The disclosed quantity for the order.
            validity (str): The validity of the order.

        Returns:
            dict: The response containing the status of the modification.
        """
        endpoint = f'/forever/orders/{order_id}'
        payload = {
            "orderId": str(order_id),
            "orderFlag": order_flag,
            "orderType": order_type,
            "legName": leg_name,
            "quantity": quantity,
            "price": price,
            "disclosedQuantity": disclosed_quantity,
            "triggerPrice": trigger_price,
            "validity": validity
        }
        return self.dhan_http.put(endpoint, payload)

    def cancel_forever(self, order_id):
        """Delete Forever orders using the order id of an order."""
        endpoint = f'/forever/orders/{order_id}'
        return self.dhan_http.delete(endpoint)

    def get_forever(self):
        """Retrieve a list of all existing Forever Orders."""
        endpoint = '/forever/orders'
        return self.dhan_http.get(endpoint)

    def generate_tpin(self):
        """
        Generate T-Pin on registered mobile number.

        Returns:
            dict: The response containing the status of T-Pin generation.
        """
        endpoint = '/edis/tpin'
        response = self.dhan_http.get(endpoint)
        response['data'] = ''
        # ToDo: This is inconsistent. If success then data should be set and not remarks field
        if response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value:
            response['remarks'] = dhanhq.OTP_SENT
        else:
            # ToDo: Why this redundant code here?
            response['remarks'] = 'status code : ' + response['remarks']['error_code']
        return response

    def open_browser_for_tpin(self, isin, qty, exchange, segment='EQ', bulk=False):
        """
        Opens the default web browser to enter T-Pin.

        Args:
            isin (str): The ISIN of the security.
            qty (int): The quantity of the security.
            exchange (str): The exchange where the security is listed.
            segment (str): The segment of the exchange (default is 'EQ').
            bulk (bool): Flag for bulk operations (default is False).

        Returns:
            dict: The response containing the status of the operation.
        """
        endpoint = '/edis/form'
        payload = {
            "isin": isin,
            "qty": qty,
            "exchange": exchange,
            "segment": segment,
            "bulk": bulk
        }
        response = self.dhan_http.post(endpoint, payload)
        if response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value:
            return response

        data = json_loads(response['data'])
        form_html = data['edisFormHtml']  # data['edisFormHtml']
        form_html = form_html.replace('\\', '')
        # print(form_html)
        self._save_as_temp_html_file_and_open_in_browser(form_html)
        return response

    def edis_inquiry(self, isin):
        """
        Inquire about the eDIS status of the provided ISIN.

        Args:
            isin (str): The ISIN to inquire about.

        Returns:
            dict: The response containing inquiry results.
        """
        endpoint = f'/edis/inquire/{isin}'
        return self.dhan_http.get(endpoint)

    def kill_switch(self, action):
        """
        Control kill switch for user, which will disable trading for current trading day.

        Args:
            action (str): 'activate' or 'deactivate' to control the kill switch.

        Returns:
            dict: Status of Kill Switch for account.
        """
        action = action.upper()
        endpoint = f'/killswitch?killSwitchStatus={action}'
        # ToDo: This should have been an Update request aka HTTP-PUT and not HTTP-POST
        return self.dhan_http.post(endpoint)

    def get_fund_limits(self):
        """
        Get all information of your trading account like balance, margin utilized, collateral, etc.

        Returns:
            dict: The response containing fund limits data.
        """
        endpoint = '/fundlimit'
        return self.dhan_http.get(endpoint)

    def margin_calculator(self, security_id, exchange_segment, transaction_type, quantity, product_type, price,
                          trigger_price=0):
        """
        Calculate the margin required for a trade based on the provided parameters.

        Args:
            security_id (str): The ID of the security for which the margin is to be calculated.
            exchange_segment (str): The exchange segment (e.g., NSE_EQ) where the trade will be executed.
            transaction_type (str): The type of transaction (BUY/SELL).
            quantity (int): The quantity of the security to be traded.
            product_type (str): The product type (e.g., CNC, INTRA) of the trade.
            price (float): The price at which the trade will be executed.
            trigger_price (float, optional): The trigger price for the trade. Defaults to 0.

        Returns:
            dict: The response containing the margin calculation result.
        """
        endpoint = '/margincalculator'
        payload = {
            "securityId": security_id,
            "exchangeSegment": exchange_segment.upper(),
            "transactionType": transaction_type.upper(),
            "quantity": int(quantity),
            "productType": product_type.upper(),
            "price": float(price)
        }
        # ToDo: Shouldn't price and trigger_price being float vlaues be rounded to 2 or 3 decimal places as precision??
        if trigger_price > 0:
            payload["triggerPrice"] = float(trigger_price)
        elif trigger_price == 0:
            payload["triggerPrice"] = 0.0

        return self.dhan_http.post(endpoint, payload)

    def get_trade_book(self, order_id=None):
        """
        Retrieve a list of all trades executed in a day.

        Args:
            order_id (str, optional): The ID of the specific order to retrieve trades for.

        Returns:
            dict: The response containing trade book data.
        """
        # ToDo: This is bad practice abusing REST principles.
        #  This should be broken into two different methods with appropriate REST convention-based URL.
        endpoint = f'/trades/{order_id if order_id is not None else ""}'
        return self.dhan_http.get(endpoint)

    def get_trade_history(self, from_date, to_date, page_number=0):
        """
        Retrieve the trade history for a specific date range.

        Args:
            from_date (str): The start date for the trade history.
            to_date (str): The end date for the trade history.
            page_number (int): The page number for pagination.

        Returns:
            dict: The response containing trade history data.
        """
        endpoint = f'/trades/{from_date}/{to_date}/{page_number}'
        return self.dhan_http.get(endpoint)

    def ledger_report(self, from_date, to_date):
        """
        Retrieve the ledger details for a specific date range.

        Args:
            from_date (str): The start date for the trade history.
            to_date (str): The end date for the trade history.

        Returns:
            dict: The response containing ledger details data.
        """
        endpoint = f'/ledger?from-date={from_date}&to-date={to_date}'
        return self.dhan_http.get(endpoint)

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
            # Raising and catching an exception in same method is bad practice. Replaced it with this clean code
            err = "expiry_code value must be ['0','1','2','3']"
            logging.error('Exception in dhanhq>>intraday_history_minute_charts: %s', err)
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

    def fetch_security_list(self, mode='compact', filename='security_id_list.csv'):
        """
        Fetch CSV file from dhan based on the specified mode and save it to the current directory.

        Args:
            mode (str): The mode to fetch the CSV ('compact' or 'detailed').
            filename (str): The name of the file to save the CSV as (default is 'data.csv').

        Returns:
            pd.DataFrame: The DataFrame containing the CSV data.
        """
        import pandas as pd
        try:
            if mode == 'compact':
                csv_url = self.COMPACT_CSV_URL
            elif mode == 'detailed':
                csv_url = self.DETAILED_CSV_URL
            else:
                raise ValueError("Invalid mode. Choose 'compact' or 'detailed'.")

            response = requests.get(csv_url)
            response.raise_for_status()

            with open(filename, 'wb') as f:
                f.write(response.content)
            df = pd.read_csv(filename)
            return df
        except Exception as e:
            logging.error('Exception in dhanhq>>fetch_security_list: %s', e)
            return None

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

    def convert_to_date_time(self, epoch):
        """
        Convert EPOCH time to Python datetime object in IST.

        Args:
            epoch (int): The EPOCH time to convert.

        Returns:
            datetime: Corresponding datetime object in IST.
        """
        IST = timezone(timedelta(hours=5, minutes=30))
        dt = datetime.fromtimestamp(epoch, IST)

        if dt.time() == datetime.min.time():
            return dt.date()
        return dt
