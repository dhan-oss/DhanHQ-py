"""
    The marketfeed class is designed to facilitate asynchronous communication with the DhanHQ API via WebSocket. 
    It enables users to subscribe to market data for a list of instruments and receive real-time updates.

    :copyright: (c) 2024 by Dhan.
    :license: see LICENSE for details.
"""

import websockets
import asyncio
import json
import struct
from datetime import datetime

# Constants
"""WebSocket URL for DhanHQ Live Market Feed"""
WSS_URL = 'wss://api-feed.dhan.co'

"""Constants for Exchange Segment"""
IDX = 0
NSE = 1
NSE_FNO = 2
NSE_CURR = 3
BSE = 4
MCX = 5
BSE_CURR = 7
BSE_FNO = 8

"""Constants for Request Code"""
Ticker = 15
Quote = 17
Depth = 19


class DhanSDKHelper:
    def __init__(self, sdk_instance):
        self.sdk_instance = sdk_instance

    """Callback function executed when the WebSocket connection is established."""
    async def on_connection_established(self, websocket):
        if self.sdk_instance.on_connect:
            await self.sdk_instance.on_connect(self.sdk_instance)

    """Callback function executed when a message is received."""
    async def on_message_received(self, response):
        if self.sdk_instance.on_message:
            await self.sdk_instance.on_message(self.sdk_instance, response)

    """Callback function executed when the WebSocket connection is closed."""
    async def on_close(self, websocket, close_status=None, close_msg=None):
        print(f"WebSocket closed with status {close_status}: {close_msg}")
        await websocket.close()
        self.ws = None



class DhanFeed:
    def __init__(self, client_id, access_token, 
                 instruments, subscription_code, 
                 on_connect=None, 
                 on_message=None, 
                 on_close=None):
        """Initializes the DhanSDK instance with user credentials, instruments to subscribe, and callback functions."""
        
        self.client_id = client_id
        self.access_token = access_token
        self.instruments = instruments
        self.subscription_code = subscription_code
        self.data = ""
        self._is_first_connect = True
        self.ws = None
        self.on_ticks = None
        self.on_message = on_message
        self.on_close = on_close
        self.on_connect = on_connect
        self.loop = asyncio.get_event_loop()

        if self.on_connect:
            self.connect()

    def run_forever(self):
        """Starts the WebSocket connection and runs the event loop."""
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        """Initiates the connection to the Websockets"""
        if not self.ws or self.ws.closed:
            self.ws = await websockets.connect(WSS_URL)
            helper = DhanSDKHelper(self)
            await helper.on_connection_established(self.ws)
            await self.authorize()
            await self.subscribe_instruments()

            # Handling incoming messages in a loop to keep the connection open
            while True:
                try:
                    response = await self.ws.recv()
                    self.data = self.process_data(response)
                    await helper.on_message_received(self.data)
                except websockets.exceptions.ConnectionClosed:
                    print("Connection has been closed")
                    break

    async def authorize(self):
        """Establishes the WebSocket connection and authorizes the user"""
        try:
            helper = DhanSDKHelper(self)
            await helper.on_connection_established(self.ws)

            # Authorization packet creation
            api_access_token = self.access_token.encode('utf-8')
            api_access_token = self.pad_with_zeros(api_access_token, 500)
            authentication_type = "2P".encode('utf-8')
            payload = api_access_token + authentication_type
            
            feed_request_code = 11
            message_length = 83 + len(api_access_token) + len(authentication_type)
            client_id = self.client_id.encode('utf-8')
            client_id = self.pad_with_zeros(client_id, 30)
            dhan_auth = b"\0" * 50
            header = struct.pack('<bH30s50s', feed_request_code, message_length, client_id, dhan_auth)

            authorization_packet = header + payload

            # Send authorization packet
            await self.ws.send(authorization_packet)
            self.is_authorized = True

        except Exception as e:
            print(f"Authorization failed: {e}")
            self.is_authorized = False
        
    async def subscribe_instruments(self):
        """Subscribe Instruments on the Open Websocket"""
        if not self.is_authorized:
            print("Not authorized. Please authorize first.")
            return

        # Subscription packet creation
        subscription_packet = self.create_subscription_packet(self.instruments, self.subscription_code)
        await self.ws.send(subscription_packet)

    def process_data(self, data):
        """Read binary data and initiate processing in received format"""
        first_byte = struct.unpack('<B', data[0:1])[0]
        if first_byte == 2:
            return self.process_ticker(data)
        elif first_byte == 3:
            return self.process_market_depth(data)
        elif first_byte == 4:
            return self.process_quote(data)
        elif first_byte == 5:
            return self.process_oi(data)
        elif first_byte == 6:
            return self.process_prev_close(data)
        elif first_byte == 7:
            return self.process_status(data)
        elif first_byte == 50:
            return self.server_disconnection(data)

    def process_ticker(self, data):
        """Parse and process Ticker Data"""
        unpack_ticker = [struct.unpack('<BHBIfI', data[0:16])]
        # Assign unpacked data to fields
        ticker_data = {
            "type" : 'Ticker Data',
            "exchange_segment" : unpack_ticker[0][2],
            "security_id" : unpack_ticker[0][3],
            "LTP" : "{:.2f}".format(unpack_ticker[0][4]),
            "LTT" : self.utc_time(unpack_ticker[0][5])
        } 
        return ticker_data
    
    def process_prev_close(self, data):
        """Parse and process Previous Day Data"""
        unpack_pclose = [struct.unpack('<BHBIfI', data[0:16])]
        # Assign unpacked data to fields
        prev_close = {
            "type" : 'Previous Close',
            "exchange_segment" : unpack_pclose[0][2],
            "security_id" : unpack_pclose[0][3],
            "prev_close" : "{:.2f}".format(unpack_pclose[0][4]),
            "prev_OI" : unpack_pclose[0][5]
        } 
        return prev_close

    def process_market_depth(self, data):
        """Parse and process Market Depth Data"""
        market_data = [struct.unpack('<BHBIf100s', data[0:112])]
        market_data_list = list(market_data[0][0:5])
        market_depth_binary = market_data[0][5]
        packet_format = '<IIHHff'

        for i in range(5):
            start_idx = i * struct.calcsize(packet_format)
            end_idx = start_idx + struct.calcsize(packet_format)
            current_packet = struct.unpack(packet_format, market_depth_binary[start_idx:end_idx])
            market_data_list.append(current_packet)
        exchange_segment = market_data_list[2]
        sec_id = market_data_list[3]
        ltp = market_data_list[4]
        depth1 = market_data_list[5]
        depth2 = market_data_list[6]
        depth3 = market_data_list[7]
        depth4 = market_data_list[8]
        depth5 = market_data_list[9]
        depth = [{"bid_quantity": depth1[0], "ask_quantity": depth1[1], "bid_orders": depth1[2], "ask_orders": depth1[3],
                  "bid_price": depth1[4], "ask_price": depth1[5]},
                 {"bid_quantity": depth2[0], "ask_quantity": depth2[1], "bid_orders": depth2[2], "ask_orders": depth2[3],
                  "bid_price": depth2[4], "ask_price": depth2[5]},
                 {"bid_quantity": depth3[0], "ask_quantity": depth3[1], "bid_orders": depth3[2], "ask_orders": depth3[3],
                  "bid_price": depth3[4], "ask_price": depth3[5]},
                 {"bid_quantity": depth4[0], "ask_quantity": depth4[1], "bid_orders": depth4[2], "ask_orders": depth4[3],
                  "bid_price": depth4[4], "ask_price": depth4[5]},
                 {"bid_quantity": depth5[0], "ask_quantity": depth5[1], "bid_orders": depth5[2], "ask_orders": depth5[3],
                  "bid_price": depth5[4], "ask_price": depth5[5]}]

        market_depth = {
            "type" : 'Market Depth',
            "exchange_segment" : exchange_segment,
            "security_id" : sec_id,
            "LTP" : ltp,
            "depth" : depth
                   }
        return market_depth

    def process_quote(self, data):
        """Parse and process Quote Data"""
        unpack_quote = [struct.unpack('<BHBIfHIfIIIffff', data[0:50])]
        quote_data = {
            "type" : 'Quote Data',
            "exchange_segment" : unpack_quote[0][2],
            "security_id": unpack_quote[0][3],
            "LTP": "{:.2f}".format(unpack_quote[0][4]),
            "LTQ" : unpack_quote[0][5],
            "LTT" : self.utc_time(unpack_quote[0][6]),
            "avg_price" : "{:.2f}".format(unpack_quote[0][7]),
            "volume" : unpack_quote[0][8],
            "total_sell_quantity" : unpack_quote[0][9],
            "total_buy_quantity" : unpack_quote[0][10],
            "open" : "{:.2f}".format(unpack_quote[0][11]),
            "close": "{:.2f}".format(unpack_quote[0][12]),
            "high": "{:.2f}".format(unpack_quote[0][13]),
            "low": "{:.2f}".format(unpack_quote[0][14])
        }
        return quote_data
    
    def process_oi(self, data):
        """Parse and process OI Data"""
        unpack_oi = [struct.unpack('<BHBII', data[0:12])]
        oi_data = {
            "type" : 'OI Data',
            "exchange_segment" : unpack_oi[0][2],
            "security_id": unpack_oi[0][3],
            "OI": unpack_oi[0][4]
        }
        return oi_data
    
    def process_status(self, data):
        """Parse and process market status"""
        unpack_status = [struct.unpack('<BHBI', data[0:8])]
        market_status = "Markets Open"
        return market_status
    
    def server_disconnection(self, data):
        """Parse and process server disconnection error"""
        disconnection_packet = [struct.unpack('<BHBIH', data[0:10])]
        self.on_close = False
        if disconnection_packet[0][4] == 805:
            print ("Disconnected: No. of active websocket connections exceeded")
            self.on_close = True
        elif disconnection_packet[0][4] == 806:
            print ("Disconnected: Subscribe to Data APIs to continue")
            self.on_close = True
        elif disconnection_packet[0][4] == 807:
            print ("Disconnected: Access Token is expired")
            self.on_close = True
        elif disconnection_packet[0][4] == 808:
            print ("Disconnected: Invalid Client ID")
            self.on_close = True
        elif disconnection_packet[0][4] == 809:
            print ("Disconnected: Authentication Failed - check ")
            self.on_close = True
        
    async def on_connection_opened(self, websocket):
        "Callback function executed when the WebSocket connection is opened."
        await websocket.send(self.create_subscription_packet(self.instruments, subscribe=True))

        while True:
            response = await websocket.recv()
            await self.on_message_received(response)

    def pad_with_zeros(self, data, length):
        """Pads a binary data string with zeros to a specified length for server to read."""
        data = data.ljust(length, b'\0')
        return data

    def create_header(self, feed_request_code, message_length, client_id):
        """Creates header packet for the subscription packet."""
        dhan_auth = b"\0" * 50
        header = struct.pack('<bH30s50s', feed_request_code, message_length, client_id.encode('utf-8'), dhan_auth)
        return header

    def utc_time(self, epoch_time):
        """Converts EPOCH time to UTC time."""
        return datetime.utcfromtimestamp(epoch_time).strftime('%H:%M:%S')

    def create_subscription_packet(self, instruments, feed_request_code):
        """Creates the subscription packet with specified instruments and subscription code"""
        num_instruments = len(instruments)
        
        header = self.create_header(feed_request_code=self.subscription_code,
                                    message_length=83 + 4 + num_instruments * 21, 
                                    client_id=self.client_id)
        num_instruments_bytes = struct.pack('<I', num_instruments)
        instrument_info = b""
        for exchange_segment, security_id in instruments:
            instrument_info += struct.pack('<B20s', exchange_segment, security_id.encode('utf-8'))
        
        instruments = [(0, "")]
        for i in range(100 - num_instruments):
            instrument_info += struct.pack('<B20s', instruments[0][0], instruments[0][1].encode('utf-8'))

        subscription_packet = header + num_instruments_bytes + instrument_info
        return subscription_packet

    def subscribe_symbols(self, feed_request_code, symbols):
        """Function to subscribe to additional symbols."""
        unique_symbols_set = set(self.instruments)
        unique_symbols_set.update(symbols)
        self.instruments = list(unique_symbols_set)
        if self.ws and self.ws.open:
            asyncio.ensure_future(self.ws.send(self.create_subscription_packet(symbols, feed_request_code, subscribe=True)))

    def unsubscribe_symbols(self, feed_request_code, symbols):
        """Function to unsubscribe symbols from connection."""
        unique_symbols_set = set(self.instruments)
        unique_symbols_set.update(symbols)
        self.instruments = list(unique_symbols_set)
        if self.ws and self.ws.open:
            print("check it", self.instruments)
            asyncio.ensure_future(self.ws.send(self.create_subscription_packet(symbols, feed_request_code, subscribe=False)))