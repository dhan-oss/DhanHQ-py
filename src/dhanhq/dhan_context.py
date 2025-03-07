"""
    A module that has a class encapsulating connection context and connection mediums to Dhan APIs.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2025 by Dhan.
    :license: see LICENSE for details.
"""

import logging

from dhanhq.dhan_http import DhanHTTP

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

        except Exception as e:
            logging.error('Exception in dhanhq>>init : %s', e)

    def get_client_id(self):
        """
        Return client's id that is used to identify the client interacting with Dhan API
        Returns client_id that is used to identify the client interacting with Dhan API
        """
        return self.client_id

    def get_access_token(self):
        """
        Return authorization token that is used for connecting to Dhan API
        Returns access_token that is used for authorization in accessing Dhan API
        """
        return self.access_token

    def get_dhan_http(self):
        """
        Return HTTP Connection Request object that has all necessary context to connect to Dhan API

        Returns
        http_connection_request (DhanHTTP): DhanContext enabled HTTP Connection Request object
        """
        return self.dhan_http
