"""
    A class to interact with the DhanHQ APIs using HTTP protocol.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2024 by Dhan.
    :license: see LICENSE for details.
"""

import logging
from enum import Enum
from json import dumps as json_dumps, loads as json_loads
from typing import Optional

import requests


class DhanHTTP:
    """Manages API keys, connection context, and HTTP requests"""

    class HttpResponseStatus(Enum):
        """Constants for HTTP Status Codes"""
        SUCCESS = 'success'
        FAILURE = 'failure'

    class HttpMethod(Enum):
        """Constants for HTTP Requests"""
        GET = 'GET'
        POST = 'POST'
        PUT = 'PUT'
        DELETE = 'DELETE'

    HTTP_DEFAULT_TIME_OUT = 60
    API_BASE_URL = 'https://api.dhan.co/v2'

    def __init__(self, client_id :str, access_token :str, disable_ssl=False, pool=None):
        self.client_id = client_id
        self.access_token = access_token
        self.base_url = DhanHTTP.API_BASE_URL
        self.timeout = DhanHTTP.HTTP_DEFAULT_TIME_OUT
        self.header = {
            'access-token': self.access_token,
            'client-id': self.client_id,
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        self.disable_ssl = disable_ssl
        self.session = requests.Session()
        if pool:
            http_adapter = requests.adapters.HTTPAdapter(**pool) # type: ignore
            self.session.mount("https://", http_adapter)

    def _send_request(self, method :HttpMethod, endpoint :str, payload: Optional[dict]={}) -> dict:
        url = self.base_url + endpoint
        if payload:
            payload["dhanClientId"] = self.client_id
        try:
            response = getattr(self.session, method.value.lower())(url,
                                                                   data=json_dumps(payload),
                                                                   headers=self.header,
                                                                   timeout=self.timeout)
            return self._parse_response(response)
        except Exception as e:
            logging.error('Exception in DhanHQConnection.%s: %s', method.value.upper(), e)
            return {
                'status': DhanHTTP.HttpResponseStatus.FAILURE.value,
                'remarks': str(e),
                'data': '',
            }

    def _parse_response(self, response):
        """
        Parse the API's string response to return a JSON as dict.

        Args:
            response (requests.Response): The response object from the API.

        Returns:
            dict: Parsed response containing status, remarks, and data.
        """
        try:
            status = DhanHTTP.HttpResponseStatus.FAILURE.value
            remarks = ''
            data = ''
            json_response = json_loads(response.content)
            if (response.status_code >= 200) and (response.status_code <= 299):
                status = DhanHTTP.HttpResponseStatus.SUCCESS.value
                data = json_response
            else:
                remarks = {
                    'error_code': (json_response.get('errorCode')),
                    'error_type': (json_response.get('errorType')),
                    'error_message': (json_response.get('errorMessage'))
                }
        except Exception as e:
            logging.warning('Exception found in dhanhq>>find_error_code: %s', e)
            status = DhanHTTP.HttpResponseStatus.FAILURE.value
            remarks = str(e)
        return {
            'status': status,
            'remarks': remarks,
            'data': data,
        }

    def get(self, endpoint: str) -> dict:
        """
        Do HTTP-GET request to Dhan Endpoint.

        Args:
            endpoint (str): The endpoint ignoring the base URL.

        Returns:
        dict: The response in dict format.
        """
        return self._send_request(DhanHTTP.HttpMethod.GET, endpoint)

    def post(self, endpoint: str, payload: dict) -> dict:
        """
        Do HTTP-POST request to Dhan Endpoint.

        Args:
            endpoint (str): The endpoint ignoring the base URL.
            payload (dict): The payload dict contains the data that needs to be sent to the server.

        Returns:
        dict: The response in dict format.
        """
        return self._send_request(DhanHTTP.HttpMethod.POST, endpoint, payload)

    def put(self, endpoint: str, payload: dict) -> dict:
        """
        Do HTTP-PUT request to Dhan Endpoint.

        Args:
            endpoint (str): The endpoint ignoring the base URL.
            payload (dict): The payload dict contains the data that needs to be sent to the server.

        Returns:
        dict: The response in dict format.
        """
        return self._send_request(DhanHTTP.HttpMethod.PUT, endpoint, payload)

    def delete(self, endpoint: str) -> dict:
        """
        Do HTTP-DELETE request to Dhan Endpoint.

        Args:
            endpoint (str): The endpoint ignoring the base URL.

        Returns:
        dict: The response in dict format.
        """
        return self._send_request(DhanHTTP.HttpMethod.DELETE, endpoint)
