"""
    The CASFeed class streams Closing Auction Session (CAS) data from DhanHQ via WebSocket.
    Client applications send JSON subscription requests and receive little-endian binary
    packets carrying the Indicative Equilibrium Price (IEP), market depth, imbalance quantity
    and reference price for each instrument, plus indicative values for indices.

    Needs the Pro Traders Plan. Data is streamed during the closing auction session.

    :copyright: (c) 2026 by Dhan.
    :license: see LICENSE for details.
"""

import asyncio
import json
import struct

import websockets


class CASFeed:
    # Constants
    """WebSocket URL for DhanHQ CAS Live Feed"""
    cas_feed_wss = 'wss://api-feed.dhan.co'

    """Constants for Exchange Segment (same numbering as MarketFeed)"""
    IDX = 0
    NSE = 1
    NSE_FNO = 2
    NSE_CURR = 3
    BSE = 4
    MCX = 5
    BSE_CURR = 7
    BSE_FNO = 8

    EXCHANGE_SEGMENTS = {
        0: "IDX_I", 1: "NSE_EQ", 2: "NSE_FNO", 3: "NSE_CURRENCY",
        4: "BSE_EQ", 5: "MCX_COMM", 7: "BSE_CURRENCY", 8: "BSE_FNO"
    }

    """Constants for Request Code"""
    Disconnect = 12
    Subscribe = 23
    Unsubscribe = 24

    """Constants for Feed Response Code"""
    CAS_PACKET = 9
    INDEX_VALUE_PACKET = 10
    DISCONNECT_PACKET = 50

    """Packet sizes in bytes"""
    HEADER_SIZE = 8
    CAS_PACKET_SIZE = 128
    INDEX_VALUE_PACKET_SIZE = 12
    INDEX_NAME_PACKET_SIZE = 33
    DISCONNECT_PACKET_SIZE = 10

    DISCONNECT_MESSAGES = {
        805: "Connection limit exceeded.",
        806: "Subscribe to Data APIs to continue.",
        807: "Access token is expired.",
        808: "Invalid client ID.",
        809: "Authentication failed."
    }

    def __init__(self, dhan_context, instruments,
                 on_connect=None, on_message=None, on_close=None, on_error=None, on_ticks=None):
        """
        Initialize the CASFeed instance.

        Args:
            dhan_context (DhanContext): Connection context with client id and access token.
            instruments (list): List of (exchange_segment, security_id) tuples to subscribe.
                exchange_segment can be a numeric code (e.g. CASFeed.NSE) or a name
                (e.g. 'NSE_EQ'). Subscribe indices with CASFeed.IDX / 'IDX_I'.
            on_connect, on_message, on_close, on_error (callable): Optional callbacks.
            on_ticks (callable): Alias for on_message.
        """
        self.client_id = dhan_context.get_client_id()
        self.access_token = dhan_context.get_access_token()
        self.instruments = list(instruments)
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
                    if self._running and (not self.ws or self._is_ws_closed()):
                        await self.connect()
            except Exception as e:
                if not self._running:
                    break
                if self.on_error:
                    self.on_error(self, e)
                await asyncio.sleep(1)
        # Let a disconnect scheduled by close_connection() finish before the loop stops,
        # otherwise a caller waiting on it from another thread would block forever.
        pending = [t for t in asyncio.all_tasks(self.loop) if t is not asyncio.current_task()]
        if pending:
            await asyncio.wait(pending, timeout=5)

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
        if not self.ws or self._is_ws_closed():
            try:
                # version=2 is required: without it the server closes the connection right away.
                url = (f"{CASFeed.cas_feed_wss}?version=2&token={self.access_token}"
                       f"&clientId={self.client_id}&authType=2")
                self.ws = await websockets.connect(url)
                await self._send_subscription(CASFeed.Subscribe, self.instruments)
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
                await self.ws.send(json.dumps({"RequestCode": CASFeed.Disconnect}))
            except Exception:
                pass
            await self.ws.close()
        if self.on_close:
            self.on_close(self)

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
            return future.result(timeout=10)
        return self.loop.run_until_complete(self.disconnect())

    def get_exchange_segment(self, exchange_segment):
        """Return the exchange segment name for a numeric code or name."""
        if isinstance(exchange_segment, str):
            if exchange_segment in CASFeed.EXCHANGE_SEGMENTS.values():
                return exchange_segment
            raise ValueError(f"Invalid exchange segment: {exchange_segment}")
        if exchange_segment in CASFeed.EXCHANGE_SEGMENTS:
            return CASFeed.EXCHANGE_SEGMENTS[exchange_segment]
        raise ValueError(f"Invalid exchange segment: {exchange_segment}")

    def create_subscription_messages(self, request_code, instruments, batch_size=100):
        """Build JSON subscribe/unsubscribe messages in batches of up to 100 instruments."""
        messages = []
        instruments = list(instruments)
        for i in range(0, len(instruments), batch_size):
            batch = instruments[i:i + batch_size]
            messages.append({
                "RequestCode": request_code,
                "InstrumentCount": len(batch),
                "InstrumentList": [
                    {"ExchangeSegment": self.get_exchange_segment(exchange_segment),
                     "SecurityId": str(security_id)}
                    for exchange_segment, security_id in batch
                ]
            })
        return messages

    async def _send_subscription(self, request_code, instruments):
        """Send subscribe/unsubscribe messages on the open WebSocket."""
        for message in self.create_subscription_messages(request_code, instruments):
            await self.ws.send(json.dumps(message))

    def subscribe_symbols(self, symbols):
        """Subscribe to additional instruments on an already-open connection."""
        new_symbols = [s for s in symbols if s not in self.instruments]
        self.instruments.extend(new_symbols)
        if new_symbols and self.ws and not self._is_ws_closed():
            self._run_coroutine(self._send_subscription(CASFeed.Subscribe, new_symbols))

    def unsubscribe_symbols(self, symbols):
        """Unsubscribe instruments from an already-open connection."""
        removed = [s for s in symbols if s in self.instruments]
        self.instruments = [s for s in self.instruments if s not in removed]
        if removed and self.ws and not self._is_ws_closed():
            self._run_coroutine(self._send_subscription(CASFeed.Unsubscribe, removed))

    def process_data(self, data):
        """
        Parse a binary message that may contain one or more concatenated packets.

        Returns a dict when the message has one packet, else a list of dicts.
        """
        packets = []
        offset = 0
        total = len(data)
        while offset + 4 <= total:
            code = data[offset]
            if code in (CASFeed.CAS_PACKET, CASFeed.INDEX_VALUE_PACKET, CASFeed.DISCONNECT_PACKET):
                msg_length = struct.unpack('<H', data[offset + 1:offset + 3])[0]
            elif struct.unpack('<H', data[offset:offset + 2])[0] == CASFeed.INDEX_NAME_PACKET_SIZE:
                # Documented indicative index packet: message length comes first, then the code.
                msg_length = CASFeed.INDEX_NAME_PACKET_SIZE
                code = None
            else:
                break
            # Stop on malformed or truncated data instead of reading past the buffer.
            if msg_length < CASFeed.HEADER_SIZE or offset + msg_length > total:
                break
            parsed = self.process_packet(code, data[offset:offset + msg_length])
            if parsed is not None:
                packets.append(parsed)
            offset += msg_length
        if len(packets) == 1:
            return packets[0]
        return packets

    def process_packet(self, code, packet):
        """Dispatch a single packet to its type-specific parser."""
        if code is None:
            return self.process_index_name(packet)
        if code == CASFeed.CAS_PACKET and len(packet) >= CASFeed.CAS_PACKET_SIZE:
            return self.process_cas(packet)
        if code == CASFeed.INDEX_VALUE_PACKET and len(packet) >= CASFeed.INDEX_VALUE_PACKET_SIZE:
            return self.process_index_value(packet)
        if code == CASFeed.DISCONNECT_PACKET and len(packet) >= CASFeed.DISCONNECT_PACKET_SIZE:
            return self.server_disconnection(packet)
        return None

    def process_cas(self, packet):
        """Parse a CAS packet (response code 9, 128 bytes)."""
        _code, _length, exch_seg, security_id = struct.unpack('<BHBI', packet[0:8])
        iep, buy_qty, sell_qty = struct.unpack('<fii', packet[8:20])
        depth = []
        for i in range(5):
            start = 20 + i * 20
            bid_qty, ask_qty, bid_orders, ask_orders, bid_price, ask_price = \
                struct.unpack('<iihhff', packet[start:start + 20])
            depth.append({
                "bid_quantity": bid_qty,
                "ask_quantity": ask_qty,
                "bid_orders": bid_orders,
                "ask_orders": ask_orders,
                "bid_price": "{:.2f}".format(bid_price),
                "ask_price": "{:.2f}".format(ask_price)
            })
        imbalance_qty, reference_price = struct.unpack('<if', packet[120:128])
        return {
            "type": "CAS",
            "exchange_segment": exch_seg,
            "security_id": security_id,
            "IEP": "{:.2f}".format(iep),
            "total_buy_quantity": buy_qty,
            "total_sell_quantity": sell_qty,
            "depth": depth,
            "imbalance_quantity": imbalance_qty,
            "reference_price": "{:.2f}".format(reference_price)
        }

    def process_index_value(self, packet):
        """Parse an indicative index value packet (response code 10, 12 bytes)."""
        _code, _length, exch_seg, security_id, value = struct.unpack('<BHBIf', packet[0:12])
        return {
            "type": "CAS Index",
            "exchange_segment": exch_seg,
            "security_id": security_id,
            "indicative_value": "{:.2f}".format(value)
        }

    def process_index_name(self, packet):
        """Parse the documented indicative index packet (33 bytes, message length first)."""
        _length, code, exch_seg, name, value = struct.unpack('<HBB21sd', packet[0:33])
        return {
            "type": "CAS Index",
            "response_code": code,
            "exchange_segment": exch_seg,
            "index_name": name.decode('utf-8', errors='ignore').strip('\x00 '),
            "indicative_value": "{:.2f}".format(value)
        }

    def server_disconnection(self, packet):
        """Parse a server disconnection packet (response code 50, 10 bytes)."""
        _code, _length, exch_seg, security_id, reason = struct.unpack('<BHBIH', packet[0:10])
        if self.on_close:
            self.on_close(self)
        return {
            "type": "Disconnect",
            "exchange_segment": exch_seg,
            "security_id": security_id,
            "error_code": reason,
            "message": CASFeed.DISCONNECT_MESSAGES.get(reason, "Unknown error.")
        }
