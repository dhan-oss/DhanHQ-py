"""
    The marketfeed class is designed to facilitate asynchronous communication with the DhanHQ API via WebSocket.
    It enables users to subscribe to market data for a list of instruments and receive real-time updates.

    :copyright: (c) 2024 by Dhan.
    :license: see LICENSE for details.
"""

import websockets
import asyncio
import struct
from datetime import datetime
from collections import defaultdict
import json

# Constants
"""WebSocket URL for DhanHQ Live Market Feed"""
market_feed_wss = 'wss://api-feed.dhan.co'

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
Full = 21


class DhanFeed:
    def __init__(self, client_id, access_token, instruments, version='v1'):
        """Initializes the DhanFeed instance with user credentials, instruments to subscribe, and callback functions."""

        self.client_id = client_id
        self.access_token = access_token
        self.instruments = instruments
        self.data = ""
        self._is_first_connect = True
        self.ws = None
        self.on_ticks = None
        self.loop = asyncio.get_event_loop()
        self.version = version

    def run_forever(self):
        """Starts the WebSocket connection and runs the event loop."""
        self.loop.run_until_complete(self.connect())

    def get_data(self): 
        """Fetch instruments data while the event loop is open."""
        return self.loop.run_until_complete(self.get_instrument_data()) 

    def close_connection(self): 
        """Close WebSocket connection with this."""
        return self.loop.run_until_complete(self.disconnect()) 

    async def connect(self):
        """Initiates the connection to the Websockets."""
        if not self.ws or self.ws.closed:
            if self.version == 'v1':
                self.ws = await websockets.connect(market_feed_wss)
                await self.authorize()
            elif self.version == 'v2':
                url = f"{market_feed_wss}?version=2&token={self.access_token}&clientId={self.client_id}&authType=2"
                self.ws = await websockets.connect(url)
            else:
                raise ValueError(f"Unsupported version: {self.version}")
            await self.subscribe_instruments()

    async def get_instrument_data(self):
        """Fetches data and initiates process for conversion."""
        response = await self.ws.recv()
        self.data = self.process_data(response)
        return self.data

    async def disconnect(self):
        """Closes the WebSocket connection and sends a disconnect message."""
        if self.ws:
            if self.version == 'v2':
                disconnect_message = {
                    "RequestCode": 12
                }
                await self.ws.send(json.dumps(disconnect_message))
                header_message = self.create_header(feed_request_code=12, message_length=83, client_id=self.client_id)
                await self.ws.send(header_message)
        print("Connection closed!")

    async def authorize(self):
        """Establishes the WebSocket connection and authorizes the user"""
        if self.version != 'v1':
            print("Authorization not needed for this version.")
            self.is_authorized = True
            return
        try:
            print("Authorizing...")

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
            print("Authorization successful!")
        except Exception as e:
            print(f"Authorization failed: {e}")
            self.is_authorized = False


    """Creating Instruments List to be subscribed"""
    def validate_and_process_tuples(self, tuples_list, batch_size=100):
        """Create a list of all instruments to be added and add in batches of 100"""
        # Check if all tuples have the same size (either all size 2 or all size 3)
        tuple_lengths = set(len(tup) for tup in tuples_list)
        if len(tuple_lengths) > 1:
            raise ValueError("All tuples must be of the same size, either all 2 or all 3.")

        # Assign default type 15 to tuples of size 2
        processed_tuples = []
        for tup in tuples_list:
            if len(tup) == 2:
                processed_tuples.append((tup[0], tup[1], 15))
            else:
                processed_tuples.append(tup)

        # Eliminate duplicate tuples
        processed_tuples = list(set(processed_tuples))

        # Separate tuples by type and prepare for batching
        batches = defaultdict(list)
        for tup in processed_tuples:
            exchange, instrument_id, type_ = tup
            if self.version == 'v1' and type_ not in [15, 17, 19]:
                raise ValueError(f"Invalid request mode for v1. Only Ticker, Quote, and Depth packet are allowed.")
            if self.version == 'v2' and type_ not in [15, 17, 21]:
                raise ValueError(f"Invalid request mode for v2. Only Ticker, Quote, and Full packet are allowed.")
            batches[type_].append((exchange, instrument_id))

        # Create the final dictionary with batches of the specified size
        final_dict = {}
        for type_ in [15, 17, 19, 21]:
            type_batches = [batches[type_][i:i+batch_size] for i in range(0, len(batches[type_]), batch_size)]
            final_dict[str(type_)] = type_batches

        return final_dict

    async def subscribe_instruments(self):
        """Subscribe Instruments on the Open Websocket"""
        if self.version == 'v1':
            if not self.is_authorized:
                print("Not authorized. Please authorize first.")
                return

            # Subscription packet creation
            group_size = 100

            new_instrument_list = self.validate_and_process_tuples(self.instruments, group_size)

            if new_instrument_list != {}:
                for instrument_type in new_instrument_list:
                    if new_instrument_list[instrument_type] != []:
                        for instrument_group in new_instrument_list[instrument_type]:
                            self.subscription_code = int(instrument_type)
                            subscription_packet = self.create_subscription_packet(instrument_group, self.subscription_code)
                            await self.ws.send(subscription_packet)
        elif self.version == 'v2':
            new_instrument_list = self.validate_and_process_tuples(self.instruments)
            for instrument_type, instrument_groups in new_instrument_list.items():
                for instrument_group in instrument_groups:
                    # Split the instrument group into batches of 100
                    for i in range(0, len(instrument_group), 100):
                        batch = instrument_group[i:i+100]
                        subscription_message = {
                            "RequestCode": int(instrument_type),
                            "InstrumentCount": len(batch),
                            "InstrumentList": [
                                {
                                    "ExchangeSegment": self.get_exchange_segment(ex),
                                    "SecurityId": token
                                } for ex, token in batch
                            ]
                        }
                        await self.ws.send(json.dumps(subscription_message))

    def get_exchange_segment(self, exchange_code):
        """Convert numeric exchange code to string representation"""
        exchange_map = {
            0: "IDX_I",
            1: "NSE_EQ",
            2: "NSE_FNO",
            3: "NSE_CURRENCY",
            4: "BSE_EQ",
            5: "MCX_COMM",
            7: "BSE_CURRENCY",
            8: "BSE_FNO"
        }
        return exchange_map.get(exchange_code, str(exchange_code))

    def process_data(self, data):
        """Read binary data and initiate processing in received format"""
        first_byte = struct.unpack('<B', data[0:1])[0]
        self.on_close = False
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
        elif first_byte == 8:
            return self.process_full(data)
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

        exchange_segment = market_data_list[2]
        sec_id = market_data_list[3]
        ltp = market_data_list[4]

        # Process Market Depth
        market_depth_binary = market_data[0][5]
        packet_format = '<IIHHff'
        packet_size = struct.calcsize(packet_format)
        depth = []
        for i in range(5):
            start_idx = i * packet_size
            end_idx = start_idx + packet_size
            current_packet = struct.unpack(packet_format, market_depth_binary[start_idx:end_idx])
            
            depth.append({
                "bid_quantity": current_packet[0],
                "ask_quantity": current_packet[1],
                "bid_orders": current_packet[2],
                "ask_orders": current_packet[3],
                "bid_price": "{:.2f}".format(current_packet[4]),
                "ask_price": "{:.2f}".format(current_packet[5])
            })

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
    
    def process_full(self, data):
        """Parse and process Full Packet Data"""
        unpack_full = [struct.unpack('<BHBIfHIfIIIIIIffff100s', data[0:162])]

        # Processing Market Depth in Full Packet
        market_depth_binary = unpack_full[0][18]
        packet_format = '<IIHHff'
        packet_size = struct.calcsize(packet_format)

        depth = []
        for i in range(5):
            start_idx = i * packet_size
            end_idx = start_idx + packet_size
            current_packet = struct.unpack(packet_format, market_depth_binary[start_idx:end_idx])
            
            depth.append({
                "bid_quantity": current_packet[0],
                "ask_quantity": current_packet[1],
                "bid_orders": current_packet[2],
                "ask_orders": current_packet[3],
                "bid_price": "{:.2f}".format(current_packet[4]),
                "ask_price": "{:.2f}".format(current_packet[5])
            })

        full_packet = {
            "type" : 'Full Data',
            "exchange_segment" : unpack_full[0][2],
            "security_id": unpack_full[0][3],
            "LTP": "{:.2f}".format(unpack_full[0][4]),
            "LTQ" : unpack_full[0][5],
            "LTT" : self.utc_time(unpack_full[0][6]),
            "avg_price" : "{:.2f}".format(unpack_full[0][7]),
            "volume" : unpack_full[0][8],
            "total_sell_quantity" : unpack_full[0][9],
            "total_buy_quantity" : unpack_full[0][10],
            "OI" : unpack_full[0][11],
            "oi_day_high" : unpack_full[0][12],
            "oi_day_low" : unpack_full[0][13],
            "open" : "{:.2f}".format(unpack_full[0][14]),
            "close": "{:.2f}".format(unpack_full[0][15]),
            "high": "{:.2f}".format(unpack_full[0][16]),
            "low": "{:.2f}".format(unpack_full[0][17]),
            "depth": depth
        }
        return full_packet


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

        header = self.create_header(feed_request_code = feed_request_code, 
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
    
    def subscribe_symbols(self, symbols): 
        """Function to subscribe to additional symbols when connection is already established."""
        # Update the instruments list
        unique_symbols_set = set(self.instruments)
        unique_symbols_set.update(symbols)
        self.instruments = list(unique_symbols_set)

        # If the WebSocket is open, send the subscription packet for the new symbols
        if self.ws and not self.ws.closed:
            # Prepare the instruments list for subscription
            group_size = 100
            new_instrument_list = self.validate_and_process_tuples(symbols, group_size)

            if self.version == 'v1':
                for instrument_type in new_instrument_list:
                    if new_instrument_list[instrument_type]:
                        for instrument_group in new_instrument_list[instrument_type]:
                            subscription_packet = self.create_subscription_packet(instrument_group, int(instrument_type))
                            asyncio.ensure_future(self.ws.send(subscription_packet))
            elif self.version == 'v2':
                new_instrument_list = self.validate_and_process_tuples(symbols)
                for instrument_type, instrument_groups in new_instrument_list.items():
                    for instrument_group in instrument_groups:
                        for i in range(0, len(instrument_group), 100):
                            batch = instrument_group[i:i+100]
                            subscription_message = {
                                "RequestCode": int(instrument_type),
                                "InstrumentCount": len(batch),
                                "InstrumentList": [
                                    {
                                        "ExchangeSegment": self.get_exchange_segment(ex),
                                        "SecurityId": token
                                    } for ex, token in batch
                                ]
                            }
                            asyncio.ensure_future(self.ws.send(json.dumps(subscription_message)))

    def unsubscribe_symbols(self, symbols): 
        """Function to unsubscribe symbols from connection when connection is already active."""
        # Update the instruments list by removing the specified symbols
        unique_symbols_set = set(self.instruments)
        unique_symbols_set.difference_update(symbols)
        self.instruments = list(unique_symbols_set)

        # If the WebSocket is open, send the unsubscription packet for the symbols
        if self.ws and not self.ws.closed:
            # Prepare the instruments list for unsubscription
            group_size = 100
            instrument_list_to_unsubscribe = self.validate_and_process_tuples(symbols, group_size)

            if self.version == 'v1':
            # Send unsubscription packets for the removed symbols
                for instrument_type in instrument_list_to_unsubscribe:
                    if instrument_list_to_unsubscribe[instrument_type]:
                        for instrument_group in instrument_list_to_unsubscribe[instrument_type]:
                            # Use the original instrument_type for grouping, but increment for the actual request
                            unsubscription_packet = self.create_subscription_packet(instrument_group, int(instrument_type) + 1)
                            asyncio.ensure_future(self.ws.send(unsubscription_packet))
            
            elif self.version == 'v2':
                for instrument_type, instrument_groups in instrument_list_to_unsubscribe.items():
                    for instrument_group in instrument_groups:
                        for i in range(0, len(instrument_group), 100):
                            batch = instrument_group[i:i+100]
                            unsubscription_message = {
                                # Use the incremented instrument_type for the actual request
                                "RequestCode": int(instrument_type) + 1,
                                "InstrumentCount": len(batch),
                                "InstrumentList": [
                                    {
                                        "ExchangeSegment": self.get_exchange_segment(ex),
                                        "SecurityId": token
                                    } for ex, token in batch
                                ]
                            }
                            asyncio.ensure_future(self.ws.send(json.dumps(unsubscription_message)))