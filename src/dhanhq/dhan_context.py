"""
    A module that has a class encapsulating connection context and connection mediums to Dhan APIs.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2024 by Dhan.
    :license: see LICENSE for details.
"""

import logging

from dhanhq.dhan_http import DhanHTTP
#from dhanhq.dhan_websocket import DhanHQWebSocket # If you have a WebSocket class

class DhanContext:
    """
        A class that encapsulates connection context to Dhan APIs like client-id, access-tocken, base-url
        and passes this to all the connection protocols like http and websocket that it is composed of.
    """

    def __init__(self, client_id, access_token, disable_ssl=False, pool=None):
        try:
            self.client_id = client_id
            self.access_token = access_token
            self.dhan_http = DhanHTTP(client_id, access_token, disable_ssl, pool)
            # self.websocket_connection = DhanWebSocket(client_id, access_token) # Initialize websocket connection
        except Exception as e:
            logging.error('Exception in dhanhq>>init : %s', e)

    def get_dhan_http(self):
        """
        Get HTTP Connection Request object that has all necessary context to connect to Dhan API

        Returns
        http_connection_request (DhanHTTP): DhanContext enabled HTTP Connection Request object
        """
        return self.dhan_http

    #def get_websocket_connection(self):
    #    return self.websocket_connection
