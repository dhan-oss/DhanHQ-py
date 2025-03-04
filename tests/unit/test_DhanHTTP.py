import json
from unittest.mock import patch

import pytest
import requests

from dhanhq.http import DhanHTTP, HTTPMethod, DhanAPIException


@pytest.fixture
def dhan_http():
    return DhanHTTP("test_client_id", "test_access_token")

@pytest.fixture
def mock_success_response():
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"data": "some data"}'
    return mock_response

@pytest.fixture
def mock_failure_response():
    mock_response = requests.Response()
    mock_response.status_code = 400
    mock_response._content = b'{"errorType": "test_error", "errorMessage": "test message"}'
    return mock_response

class TestDhanHTTP_Constructor:
    def test_init_success(self, dhan_http):
        application_json = "application/json"
        client_id = "test_client_id"
        access_token = "test_access_token"
        assert dhan_http.client_id == client_id
        assert dhan_http.access_token == access_token
        assert dhan_http.base_url == "https://api.dhan.co/v2"
        assert dhan_http.timeout == DhanHTTP.HTTP_DEFAULT_TIME_OUT
        assert dhan_http.header["access-token"] == access_token
        assert dhan_http.header["client-id"] == client_id
        assert dhan_http.header["Content-type"] == application_json
        assert dhan_http.header["Accept"] == application_json

class TestDhanHTTP_Private_MakeRequest:
    @patch("requests.Session.request")
    def test_make_request_with_payload_add_clientid_to_it(self, mock_request, dhan_http):
        """Tests POST request with a data and verifies data content."""
        endpoint = "/endpoint"
        payload = {"key": "value"}
        expected_payload = {**payload, "dhanClientId": dhan_http.client_id}
        dhan_http._make_request(HTTPMethod.POST, endpoint, data=payload)
        mock_request.assert_called_once_with('post', dhan_http.base_url + endpoint, None, expected_payload,
                                             headers=dhan_http.header, timeout=dhan_http.timeout,)

    @patch("requests.Session.request")
    def test_make_request_get_no_params(self, mock_request, dhan_http):
        """Tests GET request with no data."""
        endpoint = "/endpoint"
        dhan_http._make_request(HTTPMethod.GET, endpoint)
        mock_request.assert_called_once_with('get', dhan_http.base_url + endpoint, None, None,
                                             headers=dhan_http.header, timeout=dhan_http.timeout)

    @patch("requests.Session.request")
    def test_send_request_exception(self, mock_requests_session_post, dhan_http):
        """Tests exception handling in _send_request."""
        endpoint = "/endpoint"
        mock_requests_session_post.side_effect = requests.exceptions.ConnectionError("Test Error")
        with pytest.raises(DhanAPIException) as ex:
            dhan_http._make_request(HTTPMethod.POST, endpoint, {"test": "test"})
        assert "ConnectionError" in str(ex.value)

class TestDhanHTTP_CRUD_Methods:
    @patch("dhanhq.http.DhanHTTP._make_request")
    def test_get(self, mock_make_request, dhan_http):
        endpoint = "/endpoint"
        dhan_http.get(endpoint)
        mock_make_request.assert_called_once_with(HTTPMethod.GET, endpoint, params=None)

    @patch("dhanhq.http.DhanHTTP._make_request")
    def test_delete(self, mock_make_request, dhan_http):
        endpoint = "/endpoint"
        dhan_http.delete(endpoint)
        mock_make_request.assert_called_once_with(HTTPMethod.DELETE, endpoint)

    @patch("dhanhq.http.DhanHTTP._make_request")
    def test_put(self, mock_make_request, dhan_http):
        endpoint = "/endpoint"
        payload = {"key": "value"}
        dhan_http.put(endpoint,payload)
        mock_make_request.assert_called_once_with(HTTPMethod.PUT, endpoint, data=payload)

    @patch("dhanhq.http.DhanHTTP._make_request")
    def test_post(self, mock_make_request, dhan_http):
        endpoint = "/endpoint"
        payload = {"key": "value"}
        dhan_http.post(endpoint,payload)
        mock_make_request.assert_called_once_with(HTTPMethod.POST, endpoint, data=payload)
