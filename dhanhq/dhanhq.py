"""
    A class to interact with the DhanHQ APIs.

    This library provides methods to manage orders, retrieve market data, 
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2024 by Dhan.
    :license: see LICENSE for details.
"""

import logging
import requests
from json import loads as json_loads, dumps as json_dumps
from pathlib import Path
from webbrowser import open as web_open
from datetime import datetime, timedelta, timezone

class dhanhq:
    """DhanHQ Class to interact with REST APIs"""

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

    
    def __init__(self, client_id, access_token, disable_ssl=False, pool=None):
        """
        Initialize the dhanhq class with client ID and access token.

        Args:
            client_id (str): The client ID for the trading account.
            access_token (str): The access token for API authentication.
            disable_ssl (bool): Flag to disable SSL verification.
            pool (dict): Optional connection pool settings.
        """
        try:
            self.client_id = str(client_id)
            self.access_token = access_token
            self.base_url = 'https://api.dhan.co/v2'
            self.timeout = 60
            self.header = {
                'access-token': access_token,
                'Content-type': 'application/json',
                'Accept': 'application/json'
            }
            self.disable_ssl = disable_ssl
            requests.packages.urllib3.util.connection.HAS_IPV6 = False
            self.session = requests.Session()
            if pool:
                reqadapter = requests.adapters.HTTPAdapter(**pool)
                self.session.mount("https://", reqadapter)
        except Exception as e:
            logging.error('Exception in dhanhq>>init : %s', e)

    def _parse_response(self, response):
        """
        Parse the API response.

        Args:
            response (requests.Response): The response object from the API.

        Returns:
            dict: Parsed response containing status, remarks, and data.
        """
        try:
            status = 'failure'
            remarks = ''
            data = ''
            python_response = json_loads(response.content)
            if response.status_code == 200:
                status = 'success'
                data = python_response
            else:
                error_type = python_response.get('errorType')
                error_code = python_response.get('errorCode')
                error_message = python_response.get('errorMessage')
                remarks = {
                    'error_code': error_code,
                    'error_type' : error_type,
                    'error_message': error_message
                }
                data = python_response
        except Exception as e:
            logging.warning('Exception found in dhanhq>>find_error_code: %s', e)
            status = 'failure'
            remarks = str(e)
        return {
            'status': status,
            'remarks': remarks,
            'data': data,
        }

    def get_order_list(self):
        """
        Retrieve a list of all orders requested in a day with their last updated status.

        Returns:
            dict: The response containing order list status and data.
        """
        try:
            url = self.base_url + '/orders'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>get_order_list : %s', e)
            return {
                'status': 'failure',
                'remarks': f'Exception in dhanhq>>get_order_list : {e}',
                'data': '',
            }

    def get_order_by_id(self, order_id):
        """
        Retrieve the details and status of an order from the orderbook placed during the day.

        Args:
            order_id (str): The ID of the order to retrieve.

        Returns:
            dict: The response containing order details and status.
        """
        try:
            url = self.base_url + f'/orders/{order_id}'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>get_order_by_id : %s', e)
            return {
                'status': 'failure',
                'remarks': f'Exception in dhanhq>>get_order_by_id : {e}',
                'data': '',
            }
        
    def get_order_by_correlationID(self, correlationID):
        """
        Retrieve the order status using a field called correlation ID.

        Args:
            corelationID (str): The correlation ID provided during order placement.

        Returns:
            dict: The response containing order status.
        """
        try:
            url = self.base_url + f'/orders/external/{correlationID}'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>get_order_by_correlationID: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': ''
            }

    def modify_order(self, order_id, order_type, leg_name, quantity, price, trigger_price, disclosed_quantity, validity):
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
        try:
            url = self.base_url + f'/orders/{order_id}'
            payload = {
                "dhanClientId": self.client_id,
                "orderId": str(order_id),
                "orderType": order_type,
                "legName": leg_name,
                "quantity": quantity,
                "price": price,
                "disclosedQuantity": disclosed_quantity,
                "triggerPrice": trigger_price,
                "validity": validity
            }
            payload = json_dumps(payload)
            response = self.session.put(url, headers=self.header, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>modify_order: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

    def cancel_order(self, order_id):
        """
        Cancel a pending order in the orderbook using the order ID.

        Args:
            order_id (str): The ID of the order to cancel.

        Returns:
            dict: The response containing the status of the cancellation.
        """
        try:
            url = self.base_url + f'/orders/{order_id}'
            response = self.session.delete(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>cancel_order: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

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
        try:
            url = self.base_url + '/orders'
            payload = {
                "dhanClientId": self.client_id,
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

            payload = json_dumps(payload)
            response = self.session.post(url, data=payload, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>place_order: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
    
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
        try:
            url = self.base_url + '/orders/slicing'
            payload = {
                "dhanClientId": self.client_id,
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

            payload = json_dumps(payload)
            response = self.session.post(url, data=payload, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>place_order: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

    def get_positions(self):
        """
        Retrieve a list of all open positions for the day.

        Returns:
            dict: The response containing open positions.
        """
        try:
            url = self.base_url + f'/positions'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>get_positions: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

    def get_holdings(self):
        """
        Retrieve all holdings bought/sold in previous trading sessions.

        Returns:
            dict: The response containing holdings data.
        """
        try:
            url = self.base_url + f'/holdings'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>get_holdings: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
    def convert_position(self, from_product_type, exchange_segment, position_type, security_id, convert_qty, to_product_type):
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
        try:
            url = self.base_url + '/positions/convert' 
            payload = {
                "dhanClientId": self.client_id,
                "fromProductType": from_product_type,
                "exchangeSegment": exchange_segment,
                "positionType": position_type,
                "securityId": security_id,
                "convertQty": convert_qty,
                "toProductType": to_product_type
            }
            payload = json_dumps(payload)
            response = self.session.post(url, headers=self.header, timeout=self.timeout, data=payload)  # Changed to POST
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>convert_position: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
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
        try:
            url = self.base_url + '/forever/orders'
            payload = {
                "dhanClientId": self.client_id,
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

            if tag != None and tag != '':
                payload["correlationId"] = tag

            payload = json_dumps(payload)
            response = self.session.post(url, data=payload, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>forever_order: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
    def modify_forever(self, order_id, order_flag, order_type, leg_name, quantity, price, trigger_price, disclosed_quantity,
                       validity):
        """
        Modify a forever order based on the specified leg name. The variables that can be modified include price, quantity, order type, and validity.

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
        try:
            url = self.base_url + f'/forever/orders/{order_id}'
            payload = {
                "dhanClientId": self.client_id,
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
            payload = json_dumps(payload)
            response = self.session.put(url, headers=self.header, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>forever_modify: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
    def cancel_forever(self, order_id):
        """Delete Forever orders using the order id of an order."""
        try:
            url = self.base_url + f'/forever/orders/{order_id}'
            response = self.session.delete(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>forever_delete: %s', e)
            return {
                'status': 'failure',
                'remarks': f'Exception in dhanhq>>forever_all : {e}',
                'data': ''
            }
        
    def get_forever(self):
        """Retrieve a list of all existing Forever Orders."""
        try:
            url = self.base_url + '/forever/orders'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>forever_all : %s', e)
            return {
                'status': 'failure',
                'remarks': f'Exception in dhanhq>>forever_all : {e}',
                'data': '',
            }
        
    def generate_tpin(self):
        """
        Generate T-Pin on registered mobile number.

        Returns:
            dict: The response containing the status of T-Pin generation.
        """
        try:
            url = self.base_url + '/edis/tpin'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            if response.status_code == 202:
                return {
                    'status': 'success',
                    'remarks': 'OTP sent',
                    'data': ''
                }
            else:
                return {
                    'status': 'failure',
                    'remarks': 'status code :' + str(response.status_code),
                    'data': '',
                }
        except Exception as e:
            logging.error('Exception in dhanhq>>generate_tpin : %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

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
        try:
            url = self.base_url + '/edis/form'
            data = {
                "isin": isin,
                "qty": qty,
                "exchange": exchange,
                "segment": segment,
                "bulk": bulk
            }
            data = json_dumps(data)
            response = self.session.post(url, headers=self.header, data=data, timeout=self.timeout)
            data = json_loads(response.content)
            form_html = data['edisFormHtml']
            form_html = form_html.replace('\\', '')
            with open("temp_form.html", "w") as f:
                f.write(form_html)
            filename = f'file:\\\{Path.cwd()}\\temp_form.html'
            web_open(filename)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>open_browser_for_tpin : %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

    def edis_inquiry(self, isin):
        """
        Inquire about the eDIS status of the provided ISIN.

        Args:
            isin (str): The ISIN to inquire about.

        Returns:
            dict: The response containing inquiry results.
        """
        try:
            url = f'{self.base_url}/edis/inquire/{isin}'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>edis_inquiry : %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
    def kill_switch(self, action):
        """
        Control kill switch for user, which will disable trading for current trading day.

        Args:
            action (str): 'activate' or 'deactivate' to control the kill switch.

        Returns:
            dict: Status of Kill Switch for account.
        """
        try:
            action = action.upper()
            url = f'{self.base_url}/killswitch?killSwitchStatus={action}'
            response = self.session.post(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>kill_switch : %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
    def get_fund_limits(self):
        """
        Get all information of your trading account like balance, margin utilized, collateral, etc.

        Returns:
            dict: The response containing fund limits data.
        """
        try:
            url = self.base_url + f'/fundlimit'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>get_fund_limits: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
    def margin_calculator(self, security_id, exchange_segment, transaction_type, quantity, product_type, price, trigger_price=0):
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
        try:
            url = self.base_url + f'/margincalculator'
            payload = {
                "dhanClientId": self.client_id,
                "securityId": security_id,
                "exchangeSegment": exchange_segment.upper(),
                "transactionType": transaction_type.upper(),
                "quantity": int(quantity),
                "productType": product_type.upper(),
                "price": float(price)
            }
            if trigger_price > 0:
                payload["triggerPrice"] = float(trigger_price)
            elif trigger_price == 0:
                payload["triggerPrice"] = 0.0

            payload = json_dumps(payload)
            response = self.session.post(url, headers=self.header, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>margin_calculator: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
    def get_trade_book(self, order_id=None):
        """
        Retrieve a list of all trades executed in a day.

        Args:
            order_id (str, optional): The ID of the specific order to retrieve trades for.

        Returns:
            dict: The response containing trade book data.
        """
        try:
            if order_id is None:
                url = self.base_url + f'/trades'
            else:
                url = self.base_url + f'/trades/{order_id}'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>get_trade_book: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

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
        try:
            url = self.base_url + f'/trades/{from_date}/{to_date}/{page_number}'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>get_trade_history: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
    def ledger_report(self, from_date, to_date):
        """
        Retrieve the ledger details for a specific date range.

        Args:
            from_date (str): The start date for the trade history.
            to_date (str): The end date for the trade history.

        Returns:
            dict: The response containing ledger details data.
        """
        try:
            url = self.base_url + f'/ledger?from-date={from_date}&to-date={to_date}'
            response = self.session.get(url, headers=self.header, timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>ledger_report: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

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
        try:
            url = self.base_url + f'/charts/intraday'
            payload = {
                'securityId': security_id,
                'exchangeSegment': exchange_segment,
                'instrument': instrument_type,
                'interval': interval,
                'fromDate': from_date,
                'toDate': to_date
            }
            if interval in [1, 5, 15, 25, 60]:
                payload['interval'] = interval
            else:
                raise Exception("interval value must be ['1','5','15','25','60']")
            
            payload = json_dumps(payload)
            response = self.session.post(url, headers=self.header, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>intraday_minute_data: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

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
        try:
            url = self.base_url + f'/charts/historical'
            payload = {
                "securityId": security_id,
                "exchangeSegment": exchange_segment,
                "instrument": instrument_type,
                "expiryCode": expiry_code,
                "fromDate": from_date,
                "toDate": to_date
            }
            if expiry_code in [0, 1, 2, 3]:
                payload['expiryCode'] = expiry_code
            else:
                raise Exception("expiry_code value must be ['0','1','2','3']")

            payload = json_dumps(payload)
            response = self.session.post(url, headers=self.header, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>intraday_history_minute_charts: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
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
        try:
            url = self.base_url + f'/marketfeed/ltp'
            payload = {exchange_segment: security_id for exchange_segment, security_id in securities.items()}
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': self.access_token,
                'client-id': self.client_id
            }

            payload = json_dumps(payload)
            response = self.session.post(url, headers=headers, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>ticker_data: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
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
        try:
            url = self.base_url + f'/marketfeed/ohlc'
            payload = {exchange_segment: security_id for exchange_segment, security_id in securities.items()}
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': self.access_token,
                'client-id': self.client_id
            }

            payload = json_dumps(payload)
            response = self.session.post(url, headers=headers, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>ohlc_data: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
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
            dict: The response containing full packet including market depth, last trade, circuit limit, OHLC, OI and volume data.
        """
        try:
            url = self.base_url + f'/marketfeed/quote'
            payload = {exchange_segment: security_id for exchange_segment, security_id in securities.items()}
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': self.access_token,
                'client-id': self.client_id
            }

            payload = json_dumps(payload)
            response = self.session.post(url, headers=headers, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>quote_data: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
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
            dict: The response containing Open Interest (OI), Greeks, Volume, Last Traded Price, Best Bid/Ask, and Implied Volatility (IV) across all strikes for the specified underlying.
        """
        try:
            url = self.base_url + f'/optionchain'
            payload = {
                "UnderlyingScrip": under_security_id,
                "UnderlyingSeg": under_exchange_segment,
                "Expiry": expiry
            }
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': self.access_token,
                'client-id': self.client_id
            }

            payload = json_dumps(payload)
            response = self.session.post(url, headers=headers, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>option_chain: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }
        
    def expiry_list(self, under_security_id, under_exchange_segment):
        """
        Retrieve the dates of all expiries for a specified underlying instrument.

        Args:
            under_security_id (int): The security ID of the underlying instrument.
            under_exchange_segment (str): The exchange segment of the underlying instrument (e.g., NSE, BSE).

        Returns:
            dict: The response containing list of dates for which option expiries are present for the specified underlying instrument.
        """
        try:
            url = self.base_url + f'/optionchain/expirylist'
            payload = {
                "UnderlyingScrip": under_security_id,
                "UnderlyingSeg": under_exchange_segment
            }
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': self.access_token,
                'client-id': self.client_id
            }

            payload = json_dumps(payload)
            response = self.session.post(url, headers=headers, timeout=self.timeout, data=payload)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in dhanhq>>expiry_list: %s', e)
            return {
                'status': 'failure',
                'remarks': str(e),
                'data': '',
            }

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