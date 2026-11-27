"""
    A module that has a class encapsulating connection context and connection mediums to Dhan APIs.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2026 by Dhan.
    :license: see LICENSE for details.
"""

import logging

from dhanhq.dhan_http import DhanHTTP
from dhanhq.auth import DhanLogin

class DhanContext:
    """
        A class that encapsulates connection context to Dhan APIs like client-id, access-token, base-url
        and passes this to all the connection protocols like http and websocket that it is composed of.
    """

    def __init__(self, client_id, access_token, disable_ssl=False, pool=None, is_sandbox=False):
        try:
            self.client_id = client_id
            self.access_token = access_token
            self.is_sandbox = is_sandbox
            self.dhan_http = DhanHTTP(client_id, access_token, disable_ssl, pool, is_sandbox)
            self.dhan_login = DhanLogin(client_id)

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

    def get_dhan_login(self):
        """
        Return DhanLogin object to handle authentication

        Returns:
            DhanLogin: Object to handle authentication flows
        """
        return self.dhan_login

    def get_is_sandbox(self):
        """
        Return boolean value to identify if the connection is to sandbox or not
        Returns is_sandbox that is used to identify if the connection is to sandbox or not
        """
        return self.is_sandbox
