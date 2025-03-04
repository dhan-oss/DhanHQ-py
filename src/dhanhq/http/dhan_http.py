"""
    A class to interact with the DhanHQ APIs using HTTP protocol.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2024 by Dhan.
    :license: see LICENSE for details.
"""

import logging
from enum import Enum
from typing import Optional, Any, Dict, Union

import requests

from dhanhq.http import DhanAPIException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTTPMethod(Enum):
    """Constants for HTTP Requests"""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

class DhanHTTP:
    """Manages API keys, connection context, and HTTP requests"""

    HTTP_DEFAULT_TIME_OUT = 60
    API_BASE_URL = 'https://api.dhan.co/v2'

    def __init__(self, client_id: str, access_token: str, disable_ssl: bool=False, pool: Union[dict,None]=None):
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
        # self.session.headers.update({'k':'v'})
        if pool:
            http_adapter = requests.adapters.HTTPAdapter(**pool) # type: ignore
            self.session.mount("https://", http_adapter)


    def _make_request(self,
                      method :HTTPMethod,
                      endpoint :str,
                      params: Optional[Dict[str, Any]] = None,
                      data: Optional[Dict[str, Any]] = None,
                      **kwargs) -> Any:
        url = f'{self.base_url}{endpoint}'
        http_method = method.value.lower()
        merged_kwargs = {
            **kwargs,
            'headers': {**kwargs.get('headers', {}), **self.header},
            'timeout': self.timeout
        }

        if data is not None:
            data['dhanClientId'] = self.client_id

        try:
            response = self.session.request(http_method,url, params, data, **merged_kwargs)
            response.raise_for_status()  # Raise an exception for 4xx/5xx status codes

            # Handle non-JSON responses (e.g., 202 Accepted with no JSON body)
            if response.status_code == 202:
                return 'Request accepted for processing'

            response_json = response.json()
            return response_json #['data']
        except requests.exceptions.HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')
            raise DhanAPIException(code=str(response.status_code), message={http_err}) # type: ignore
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f'Connection error occurred: {conn_err}')
            raise DhanAPIException(code="HTTP 503: Service Unavailable: ConnectionError", message=str(conn_err))
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f'Request timed out: {timeout_err}')
            raise DhanAPIException(code="HTTP 408: Request Timeout Error", message=str(timeout_err))
        except requests.exceptions.RequestException as req_err:
            logger.error(f'An error occurred: {req_err}')
            raise DhanAPIException(code=str(response.status_code), message={req_err}) # type: ignore
        except Exception as err:
            logger.error(f'An unexpected error occurred: {err}')
            raise DhanAPIException(code="UNKNOWN_ERROR", message=str(err))


    def get(self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Do HTTP-GET request to Dhan Endpoint.
        """
        return self._make_request(HTTPMethod.GET, endpoint, params=params)


    def post(self,
             endpoint: str,
             data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Do HTTP-POST request to Dhan Endpoint.
        """
        return self._make_request(HTTPMethod.POST, endpoint, data=data)


    def put(self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Do HTTP-PUT request to Dhan Endpoint.
        """
        return self._make_request(HTTPMethod.PUT, endpoint, data=data)


    def delete(self,
               endpoint: str) -> Any:
        """
        Do HTTP-DELETE request to Dhan Endpoint.
        """
        return self._make_request(HTTPMethod.DELETE, endpoint)
