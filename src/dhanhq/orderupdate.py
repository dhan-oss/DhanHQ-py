"""
    The orderupdate class is designed to facilitate asynchronous communication with the DhanHQ API via WebSocket.
    It enables users to subscribe to market data for a list of instruments and receive real-time updates.

    :copyright: (c) 2026 by Dhan.
    :license: see LICENSE for details.
"""

import asyncio
import websockets
import json
from typing import Callable, Optional


class OrderUpdate:
    """
    A class to manage WebSocket connections for order updates.

    Attributes:
        client_id (str): The client ID for authentication.
        access_token (str): The access token for authentication.
        order_feed_wss (str): The WebSocket URL for order updates.
    """

    on_update: Optional[Callable[[dict], None]] = None

    def __init__(self, dhan_context, on_connect=None, on_close=None):
        """
        Initializes the OrderSocket with client ID and access token.

        Args:
            dhan_context: The Dhan context containing client ID and access token.
            on_connect: Optional callback when connection is established.
            on_close: Optional callback when connection is closed.
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

            if self.on_connect:
                self.on_connect(self)
        finally:
            self._connecting = False

    async def _run_async(self):
        """Internal async method to handle the connection loop."""
        await self.connect()
        while self._running:
            ws = self.ws
            try:
                if ws and not self._is_ws_closed(ws):
                    message = await asyncio.wait_for(ws.recv(), timeout=1)
                    data = json.loads(message)
                    self.handle_order_update(data)
                else:
                    await asyncio.sleep(1)
                    ws = self.ws
                    if self._running and (not ws or self._is_ws_closed(ws)):
                        await self.connect()
            except asyncio.TimeoutError:
                continue
            except websockets.ConnectionClosed:
                if self._running:
                    await asyncio.sleep(1)
                    if self._running:
                        await self.connect()
            except Exception as e:
                if self._running:
                    print(f"Error in order update: {e}")
                    await asyncio.sleep(1)

    def _is_ws_closed(self, ws=None):
        """Helper method to safely check if WebSocket is closed."""
        if ws is None:
            ws = self.ws
        if not ws:
            return True
        try:
            return getattr(ws, 'closed', False) or ws.state == websockets.protocol.State.CLOSED
        except Exception:
            return True

    async def disconnect(self):
        """Closes the WebSocket connection gracefully."""
        ws = self.ws
        self.ws = None
        if ws:
            try:
                await ws.close()
            except Exception as e:
                print(f"Error during disconnect: {e}")

        if self.on_close:
            self.on_close(self)
        print("Connection closed!")

    def close_connection(self):
        """Synchronous method to close the WebSocket connection. Thread-safe."""
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
            try:
                return future.result(timeout=5)
            except TimeoutError:
                future.cancel()
                print("Warning: disconnect timed out")
                return
        else:
            if self.loop.is_closed():
                return
            return self.loop.run_until_complete(self.disconnect())

    def run(self):
        """Blocking call to run the WebSocket connection. Handles KeyboardInterrupt gracefully."""
        if self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        self._running = True
        try:
            self.loop.run_until_complete(self._run_async())
        except KeyboardInterrupt:
            self._running = False
            if self.ws:
                self.loop.run_until_complete(self.disconnect())
            else:
                self.ws = None
            self.loop.close()

    def start(self):
        """Starts the WebSocket connection in a separate thread. Returns the thread object."""
        import threading
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

    # Keep for backward compatibility
    async def connect_order_update(self):
        """Deprecated: Use run() or start() instead."""
        self._running = True
        await self._run_async()

    def connect_to_dhan_websocket_sync(self):
        """Deprecated: Use run() or start() instead."""
        try:
            self.run()
        except Exception as e:
            print(f"Error in connect_to_dhan_websocket: {e}")
