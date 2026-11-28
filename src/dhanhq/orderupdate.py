"""
    The orderupdate class is designed to facilitate asynchronous communication with the DhanHQ API via WebSocket.
    It enables users to subscribe to market data for a list of instruments and receive real-time updates.

    :copyright: (c) 2026 by Dhan.
    :license: see LICENSE for details.
"""

import asyncio
import json
import threading
from typing import Callable, Optional
import websockets


class OrderUpdate:
    """
    A class to manage WebSocket connections for order updates.

    Attributes:
        client_id (str): The client ID for authentication.
        access_token (str): The access token for authentication.
        order_feed_wss (str): The WebSocket URL for order updates.
    """

    on_update: Optional[Callable[[dict], None]] = None

    def __init__(self, dhan_context, on_connect=None, on_close=None, on_error=None, on_update=None):
        """
        Initializes the OrderSocket with client ID and access token.

        Args:
            dhan_context: The Dhan context containing client ID and access token.
            on_connect: Optional callback when connection is established.
            on_close: Optional callback when connection is closed.
            on_error: Optional callback when an error occurs.
            on_update: Optional callback when an order update is received.
        """
        self.client_id = dhan_context.get_client_id()
        self.access_token = dhan_context.get_access_token()
        self.order_feed_wss = "wss://api-order-update.dhan.co"
        self.ws = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._running = False
        self._connecting = False
        self.on_connect = on_connect
        self.on_close = on_close
        self.on_error = on_error
        if on_update:
            self.on_update = on_update

    def _is_ws_closed(self, ws=None):
        """Helper method to safely check if WebSocket is closed."""
        if ws is None:
            ws = self.ws
        if not ws:
            return True
        try:
            if getattr(ws, 'closed', False):
                return True
            state = getattr(ws, 'state', None)
            if state is not None:
                proto = getattr(websockets, 'protocol', None)
                proto_state = getattr(proto, 'State', None)
                if proto_state and getattr(proto_state, 'CLOSED', None) == state:
                    return True
                ws_state = getattr(websockets, 'State', None)
                if ws_state and getattr(ws_state, 'CLOSED', None) == state:
                    return True
            return False
        except Exception:
            return True

    async def connect(self):
        """
        Connects to the WebSocket and authenticates.
        """
        ws = self.ws
        if ws and not self._is_ws_closed(ws):
            return

        while self._connecting:
            await asyncio.sleep(0.1)

        ws = self.ws
        if ws and not self._is_ws_closed(ws):
            return

        self._connecting = True
        try:
            self.ws = await websockets.connect(self.order_feed_wss)
            auth_message = {
                "LoginReq": {
                    "MsgCode": 42,
                    "ClientId": str(self.client_id),
                    "Token": str(self.access_token)
                },
                "UserType": "SELF"
            }

            await self.ws.send(json.dumps(auth_message))
            print(f"Sent subscribe message: {auth_message}")

            if self.on_connect and callable(self.on_connect):
                try:
                    self.on_connect(self)
                except TypeError:
                    self.on_connect()
        finally:
            self._connecting = False

    async def _process_next_message(self, ws):
        """Receives and processes a single message from the WebSocket."""
        try:
            message = await asyncio.wait_for(ws.recv(), timeout=1)
            data = json.loads(message)
            self.handle_order_update(data)
        except asyncio.TimeoutError:
            pass

    async def _handle_error(self, error):
        """Dispatches or logs an error occurring during order updates."""
        if self.on_error and callable(self.on_error):
            try:
                self.on_error(self, error)
            except TypeError:
                self.on_error(error)
        else:
            print(f"Error in order update: {error}")
        await asyncio.sleep(1)

    async def _run_async(self):
        """Internal async method to handle the connection loop."""
        await self.connect()
        while self._running:
            ws = self.ws
            try:
                if ws and not self._is_ws_closed(ws):
                    await self._process_next_message(ws)
                else:
                    await asyncio.sleep(1)
                    if self._running and self._is_ws_closed(self.ws):
                        await self.connect()
            except websockets.ConnectionClosed:
                if self._running:
                    await asyncio.sleep(1)
                    await self.connect()
            except Exception as e:
                if self._running:
                    await self._handle_error(e)

    async def disconnect(self):
        """
        Closes the WebSocket connection gracefully.
        """
        self._running = False
        ws = self.ws
        self.ws = None
        if ws:
            try:
                await ws.close()
            except Exception as e:
                print(f"Error during disconnect: {e}")

        if self.on_close and callable(self.on_close):
            try:
                self.on_close(self)
            except TypeError:
                self.on_close()
        print("Connection closed!")

    def close_connection(self):
        """
        Close the WebSocket connection synchronously.
        """
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
        else:
            if self.loop.is_closed():
                return
            return self.loop.run_until_complete(self.disconnect())

    def run(self):
        """
        Blocking call to run the WebSocket connection.
        Handles KeyboardInterrupt gracefully.
        """
        if self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        self._running = True
        try:
            self.loop.run_until_complete(self._run_async())
        except KeyboardInterrupt:
            self.close_connection()

    def start(self):
        """
        Starts the WebSocket connection in a separate thread.
        Returns the thread object.
        """
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        return t

    def handle_order_update(self, order_update):
        """
        Handles incoming order update messages.

        Args:
            order_update (dict): The order update message received from the WebSocket.
        """
        if order_update.get('Type') == 'order_alert':
            if self.on_update and callable(self.on_update):
                return self.on_update(order_update)

            data = order_update.get('Data', {})
            if "orderNo" in data:
                order_id = data["orderNo"]
                status = data.get("status", "Unknown status")
                print(f"Status: {status}, Order ID: {order_id}, Data: {data}")
            else:
                print(f"Order Update received: {data}")
        else:
            print(f"Unknown message received: {order_update}")

    async def connect_order_update(self):
        """
        Connects to the WebSocket and listens for order updates.
        Provided for backward compatibility.
        """
        self._running = True
        await self._run_async()

    def connect_to_dhan_websocket_sync(self):
        """
        Synchronously connects to the WebSocket.
        Provided for backward compatibility.
        """
        try:
            self.run()
        except Exception as e:
            print(f"Error in connect_to_dhan_websocket: {e}")
