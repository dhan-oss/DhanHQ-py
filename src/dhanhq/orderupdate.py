"""
    The orderupdate class is designed to facilitate asynchronous communication with the DhanHQ API via WebSocket.
    It enables users to subscribe to market data for a list of instruments and receive real-time updates.

    :copyright: (c) 2026 by Dhan.
    :license: see LICENSE for details.
"""

import asyncio
import json
import logging
import websockets
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class OrderUpdate:
    """
    A class to manage WebSocket connections for order updates.

    Attributes:
        client_id (str): The client ID for authentication.
        access_token (str): The access token for authentication.
        order_feed_wss (str): The WebSocket URL for order updates.
    """

    on_update: Optional[Callable[[dict], None]] = None

    def __init__(self, dhan_context):
        """
        Initializes the OrderSocket with client ID and access token.

        Args:
            client_id (str): The client ID for authentication.
            access_token (str): The access token for authentication.
        """
        self.client_id = dhan_context.get_client_id()
        self.access_token = dhan_context.get_access_token()
        self.order_feed_wss = "wss://api-order-update.dhan.co"

    async def connect_order_update(self):
        """
        Connects to the WebSocket and listens for order updates.

        This method authenticates the client and processes incoming messages.
        """
        async with websockets.connect(self.order_feed_wss) as websocket:
            auth_message = {
                "LoginReq": {
                    "MsgCode": 42,
                    "ClientId": str(self.client_id),
                    "Token": str(self.access_token)
                },
                "UserType": "SELF"
            }

            await websocket.send(json.dumps(auth_message))
            logger.debug("Sent subscribe message to order update feed")

            async for message in websocket:
                data = json.loads(message)
                self.handle_order_update(data)

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
                logger.info("Status: %s, Order ID: %s", status, order_id)
            else:
                logger.info("Order Update received: %s", data)
        else:
            logger.debug("Unknown message received: %s", order_update)

    def connect_to_dhan_websocket_sync(self):
        """
        Synchronously connects to the WebSocket.

        This method runs the asynchronous connect_order_update method in a new event loop.
        """
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(self.connect_order_update())
        except Exception as e:
            logger.error("Error in connect_to_dhan_websocket: %s", e)
        finally:
            loop.close()
