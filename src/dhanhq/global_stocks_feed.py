"""
    The GlobalStocksFeed class facilitates asynchronous communication with the DhanHQ
    Global Stocks (US) Live Feed via WebSocket. Client applications send JSON subscription
    requests and receive compact little-endian binary market-data packets in real time.

    :copyright: (c) 2026 by Dhan.
    :license: see LICENSE for details.
"""

import asyncio
import json
import struct
from datetime import datetime

import websockets


class GlobalStocksFeed:
    # Constants
    """WebSocket URL for DhanHQ Global Stocks Live Feed"""
    global_feed_wss = 'wss://global-stocks-api-feed.dhan.co/'

    """Supported exchange segment for Global Stocks"""
    INX_EQ = 'INX_EQ'

    """Constants for Request Code"""
    Disconnect = 12
    SubscribeTrade = 15
    UnsubscribeTrade = 16
    SubscribeOHLC = 17
    UnsubscribeOHLC = 18

    """Constants for Auth Type"""
    AUTH_PARTNER_CLIENT = 1
    AUTH_SELF = 2
    AUTH_PARTNER = 3

    def __init__(self, dhan_context, instruments, auth_type=AUTH_SELF,
                 on_connect=None, on_message=None, on_close=None, on_error=None, on_ticks=None):
        """
        Initialize the GlobalStocksFeed instance.

        Args:
            dhan_context (DhanContext): Connection context with client id and access token.
            instruments (list): List of tuples to subscribe. Each tuple is
                (exchange_segment, security_id) - defaults to Trade feed - or
                (exchange_segment, security_id, request_code) where request_code is
                15 (Subscribe Trade) or 17 (Subscribe OHLC).
            auth_type (int): 1 for Partner's Client, 2 for Self, 3 for Partner. Defaults to 2.
            on_connect, on_message, on_close, on_error (callable): Optional callbacks.
            on_ticks (callable): Alias for on_message.
        """
        self.client_id = dhan_context.get_client_id()
        self.access_token = dhan_context.get_access_token()
        self.instruments = instruments
        self.auth_type = auth_type
        self.data = ""
        self.ws = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Callbacks
        self.on_connect = on_connect
        self.on_message = on_message
        if not on_message and on_ticks:
            self.on_message = on_ticks
        self.on_close = on_close
        self.on_error = on_error

        self._running = False

    def run_forever(self):
        """Start the WebSocket connection and run the event loop."""
        self.loop.run_until_complete(self.connect())

    def get_data(self):
        """Fetch instrument data while the event loop is open."""
        return self.loop.run_until_complete(self.get_instrument_data())

    def run(self):
        """Blocking call that connects, receives messages and dispatches callbacks."""
        self._running = True
        try:
            self.loop.run_until_complete(self._run_async())
        except KeyboardInterrupt:
            self.close_connection()

    def start(self):
        """Start the WebSocket connection in a separate daemon thread. Returns the thread."""
        import threading
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        return t

    async def _run_async(self):
        """Internal async loop handling connection and message dispatch."""
        await self.connect()
        while self._running:
            try:
                if self.ws and not self._is_ws_closed():
                    data = await self.get_instrument_data()
                    if self.on_message:
                        self.on_message(self, data)
                else:
                    await asyncio.sleep(1)
                    if not self.ws or self._is_ws_closed():
                        await self.connect()
            except Exception as e:
                if self.on_error:
                    self.on_error(self, e)
                await asyncio.sleep(1)

    def _run_coroutine(self, coro):
        """Run coroutine in the event loop from any thread."""
        try:
            loop = asyncio.get_running_loop()
            if loop == self.loop:
                asyncio.create_task(coro)
                return
        except RuntimeError:
            pass
        asyncio.run_coroutine_threadsafe(coro, self.loop)

    def _is_ws_closed(self):
        """Safely check whether the WebSocket is closed."""
        if not self.ws:
            return True
        try:
            return getattr(self.ws, 'closed', False) or self.ws.state == websockets.protocol.State.CLOSED
        except Exception:
            return True

    async def connect(self):
        """Open the WebSocket connection and subscribe to the configured instruments."""
        if not self.ws or self.ws.state == websockets.protocol.State.CLOSED:
            try:
                url = (f"{GlobalStocksFeed.global_feed_wss}?clientId={self.client_id}"
                       f"&token={self.access_token}&authType={self.auth_type}&version=2")
                self.ws = await websockets.connect(url)
                await self.subscribe_instruments()
                if self.on_connect:
                    self.on_connect(self)
            except Exception as e:
                if self.on_error:
                    self.on_error(self, e)
                raise e
        else:
            try:
                await self.ws.ping()
            except websockets.ConnectionClosed:
                self.ws = None
                await self.connect()

    async def get_instrument_data(self):
        """Receive a binary message and process it."""
        response = await self.ws.recv()
        self.data = self.process_data(response)
        return self.data

    async def disconnect(self):
        """Send a disconnect request and close the WebSocket connection."""
        if self.ws:
            try:
                await self.ws.send(json.dumps({"requestCode": GlobalStocksFeed.Disconnect}))
            except Exception:
                pass
            await self.ws.close()
        if self.on_close:
            self.on_close(self)
        print("Connection closed!")

    def close_connection(self):
        """Close the WebSocket connection."""
        self._running = False
        try:
            loop = asyncio.get_running_loop()
            if loop == self.loop:
                asyncio.create_task(self.disconnect())
                return
        except RuntimeError:
            pass

        if self.loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.disconnect(), self.loop)
            return future.result()
        return self.loop.run_until_complete(self.disconnect())

    def _normalize_instruments(self, instruments):
        """Group instruments by request code. Tuples of size 2 default to Trade (15)."""
        batches = {}
        for tup in instruments:
            if len(tup) == 2:
                exchange_segment, security_id, request_code = tup[0], tup[1], GlobalStocksFeed.SubscribeTrade
            else:
                exchange_segment, security_id, request_code = tup
            if request_code not in (GlobalStocksFeed.SubscribeTrade, GlobalStocksFeed.SubscribeOHLC):
                raise ValueError("request_code must be 15 (Subscribe Trade) or 17 (Subscribe OHLC).")
            batches.setdefault(request_code, []).append((exchange_segment, security_id))
        return batches

    async def _send_subscription(self, request_code, instrument_pairs):
        """Send subscribe/unsubscribe messages in batches of up to 100 instruments."""
        for i in range(0, len(instrument_pairs), 100):
            batch = instrument_pairs[i:i + 100]
            message = {
                "requestCode": request_code,
                "instrumentCount": len(batch),
                "instrumentList": [
                    {"exchangeSegment": exchange_segment, "securityId": str(security_id)}
                    for exchange_segment, security_id in batch
                ]
            }
            await self.ws.send(json.dumps(message))

    async def subscribe_instruments(self):
        """Subscribe to all configured instruments on the open WebSocket."""
        for request_code, pairs in self._normalize_instruments(self.instruments).items():
            await self._send_subscription(request_code, pairs)

    def subscribe_symbols(self, symbols):
        """Subscribe to additional instruments on an already-open connection."""
        self.instruments = list(set(self.instruments) | set(symbols))
        if self.ws and not self._is_ws_closed():
            for request_code, pairs in self._normalize_instruments(symbols).items():
                self._run_coroutine(self._send_subscription(request_code, pairs))

    def unsubscribe_symbols(self, symbols):
        """Unsubscribe instruments from an already-open connection."""
        self.instruments = list(set(self.instruments) - set(symbols))
        if self.ws and not self._is_ws_closed():
            for request_code, pairs in self._normalize_instruments(symbols).items():
                # 15 -> 16 (Unsubscribe Trade), 17 -> 18 (Unsubscribe OHLC)
                self._run_coroutine(self._send_subscription(request_code + 1, pairs))

    def process_data(self, data):
        """Parse a binary message that may contain one or more concatenated packets."""
        # Error packets are standalone and start with MsgCode (50) at offset 0.
        if data and data[0] == 50:
            return self.process_error(data)

        packets = []
        offset = 0
        total = len(data)
        while offset + 11 <= total:
            msg_length = data[offset + 9]
            msg_code = data[offset + 10]
            packet = data[offset:offset + msg_length]
            parsed = self.process_packet(msg_code, packet)
            if parsed is not None:
                packets.append(parsed)
            if msg_length <= 0:
                break
            offset += msg_length
        if len(packets) == 1:
            return packets[0]
        return packets

    def _parse_header(self, packet):
        """Unpack the 11-byte packet header. Returns (exch_seg, scrip_id)."""
        exch_seg, scrip_id, _scrip_id2, _msg_length, _msg_code = struct.unpack('<BiiBB', packet[0:11])
        return exch_seg, scrip_id

    def process_packet(self, msg_code, packet):
        """Dispatch a single packet to its type-specific parser."""
        if msg_code == 1:
            return self.process_trade(packet)
        elif msg_code == 3:
            return self.process_ohlc(packet)
        elif msg_code == 29:
            return self.process_market_status(packet)
        elif msg_code == 32:
            return self.process_prev_close(packet)
        elif msg_code == 33:
            return self.process_circuit_limit(packet)
        elif msg_code == 36:
            return self.process_52_week(packet)
        return None

    def process_trade(self, packet):
        """Parse a Trade packet (MsgCode 1, 37 bytes). Price fields (LTP, ATP) are float32."""
        exch_seg, scrip_id = self._parse_header(packet)
        ltp, ltq, volume, atp, oi, ltt, lut = struct.unpack('<fhifiii', packet[11:37])
        return {
            "type": "Trade",
            "exchange_segment": exch_seg,
            "security_id": scrip_id,
            "LTP": "{:.2f}".format(ltp),
            "LTQ": ltq,
            "volume": volume,
            "ATP": "{:.2f}".format(atp),
            "OI": oi,
            "LTT": self.utc_time(ltt),
            "LUT": self.utc_time(lut)
        }

    def process_ohlc(self, packet):
        """Parse an OHLC packet (MsgCode 3, 27 bytes). O/H/L/C are float32."""
        exch_seg, scrip_id = self._parse_header(packet)
        open_, close, high, low = struct.unpack('<ffff', packet[11:27])
        return {
            "type": "OHLC",
            "exchange_segment": exch_seg,
            "security_id": scrip_id,
            "open": "{:.2f}".format(open_),
            "close": "{:.2f}".format(close),
            "high": "{:.2f}".format(high),
            "low": "{:.2f}".format(low)
        }

    def process_prev_close(self, packet):
        """Parse a Previous Close packet (MsgCode 32, 19 bytes)."""
        exch_seg, scrip_id = self._parse_header(packet)
        prev_close, prev_oi = struct.unpack('<ff', packet[11:19])
        return {
            "type": "Previous Close",
            "exchange_segment": exch_seg,
            "security_id": scrip_id,
            "prev_close": prev_close,
            "prev_OI": prev_oi
        }

    def process_circuit_limit(self, packet):
        """Parse a Circuit Limit packet (MsgCode 33, 19 bytes)."""
        exch_seg, scrip_id = self._parse_header(packet)
        upper_circuit, lower_circuit = struct.unpack('<ff', packet[11:19])
        return {
            "type": "Circuit Limit",
            "exchange_segment": exch_seg,
            "security_id": scrip_id,
            "upper_circuit": upper_circuit,
            "lower_circuit": lower_circuit
        }

    def process_52_week(self, packet):
        """Parse a 52-Week High/Low packet (MsgCode 36, 19 bytes)."""
        exch_seg, scrip_id = self._parse_header(packet)
        week_high, week_low = struct.unpack('<ff', packet[11:19])
        return {
            "type": "52 Week High Low",
            "exchange_segment": exch_seg,
            "security_id": scrip_id,
            "week_high": week_high,
            "week_low": week_low
        }

    def process_market_status(self, packet):
        """Parse a Market Status packet (MsgCode 29, 18 bytes)."""
        exch_seg, scrip_id = self._parse_header(packet)
        market_type, market_status = struct.unpack('<3si', packet[11:18])
        return {
            "type": "Market Status",
            "exchange_segment": exch_seg,
            "security_id": scrip_id,
            "market_type": market_type.decode('utf-8', errors='ignore').strip('\x00'),
            "market_status": market_status
        }

    def process_error(self, packet):
        """Parse an Error packet (MsgCode 50, 10 bytes)."""
        msg_code, _msg_length, exch_seg, scrip_id, err_code = struct.unpack('<BHBiH', packet[0:10])
        messages = {
            805: "Connection limit exceeded.",
            806: "Payment not done for broadcast.",
            807: "Token expired.",
            808: "Authentication failure.",
            809: "Invalid token."
        }
        error = {
            "type": "Error",
            "exchange_segment": exch_seg,
            "security_id": scrip_id,
            "error_code": err_code,
            "message": messages.get(err_code, "Unknown error.")
        }
        if self.on_close:
            self.on_close(self)
        return error

    def utc_time(self, epoch_time):
        """Convert EPOCH time to a UTC HH:MM:SS string."""
        return datetime.utcfromtimestamp(epoch_time).strftime('%H:%M:%S')
