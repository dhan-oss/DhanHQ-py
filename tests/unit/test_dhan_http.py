import json
from unittest.mock import patch

import pytest
import requests

from dhanhq.dhan_http import DhanHTTP

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

class TestDhan_Constructor:
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

class TestDhan_Private_ParseResponse:
    def test_parse_response_success_with_status_code_200(self, dhan_http, mock_success_response):
        json_response = dhan_http._parse_response(mock_success_response)
        assert json_response["status"] == "success"
        assert json_response["remarks"] == ""
        assert json_response["data"] == {"data": "some data"}

    def test_parse_response_success_with_status_code_299(self, dhan_http, mock_success_response):
        mock_success_response.status_code = 299
        json_response = dhan_http._parse_response(mock_success_response)
        assert json_response["status"] == "success"
        assert json_response["remarks"] == ""
        assert json_response["data"] == {"data": "some data"}

    def test_parse_response_error_with_status_code_400(self, dhan_http, mock_failure_response):
        json_response = dhan_http._parse_response(mock_failure_response)
        assert json_response["status"] == "failure"
        assert json_response["remarks"]["error_type"] == "test_error"
        assert json_response["remarks"]["error_message"] == "test message"
        assert json_response["data"] == ""

class TestDhan_Private_SendRequest:
    @patch("requests.Session.post")
    def test_send_request_with_payload_add_clientid_to_it(self,mock_requests_session_post, dhan_http):
        """Tests POST request with a payload and verifies payload content."""
        endpoint = "/endpoint"
        payload = {"key": "value"}
        dhan_http._send_request(DhanHTTP.HttpMethods.POST, endpoint, payload)
        mock_requests_session_post.assert_called_once_with(
            dhan_http.base_url + endpoint,
            data=json.dumps({**payload, "dhanClientId": dhan_http.client_id}),
            headers=dhan_http.header,
            timeout=dhan_http.timeout,
        )

    @patch("requests.Session.get")
    def test_send_request_get_no_payload(self, mock_requests_session_get, dhan_http):
        """Tests GET request with no payload."""
        endpoint = "/endpoint"
        dhan_http._send_request(DhanHTTP.HttpMethods.GET, endpoint)
        mock_requests_session_get.assert_called_once_with(
            dhan_http.base_url + endpoint,
            data=None,
            headers=dhan_http.header,
            timeout=dhan_http.timeout
        )

    @patch("requests.Session.post")
    def test_send_request_exception(self, mock_requests_session_post, dhan_http):
        """Tests exception handling in _send_request."""
        endpoint = "/endpoint"
        mock_requests_session_post.side_effect = requests.exceptions.ConnectionError("Test Error")
        response = dhan_http._send_request(DhanHTTP.HttpMethods.POST, endpoint, {"test": "test"})
        assert response['status'] == 'failure'

class TestDhan_CRUD_Methods:
    @patch("dhanhq.DhanHTTP._send_request")
    def test_get(self,mock_send_request,dhan_http):
        endpoint = "/endpoint"
        dhan_http.get(endpoint)
        mock_send_request.assert_called_once_with(DhanHTTP.HttpMethods.GET,endpoint,)

    @patch("dhanhq.DhanHTTP._send_request")
    def test_delete(self,mock_send_request,dhan_http):
        endpoint = "/endpoint"
        dhan_http.delete(endpoint)
        mock_send_request.assert_called_once_with(DhanHTTP.HttpMethods.DELETE, endpoint)

    @patch("dhanhq.DhanHTTP._send_request")
    def test_put(self,mock_send_request,dhan_http):
        endpoint = "/endpoint"
        payload = {"key": "value"}
        dhan_http.put(endpoint,payload)
        mock_send_request.assert_called_once_with(DhanHTTP.HttpMethods.PUT,endpoint,payload)

    @patch("dhanhq.DhanHTTP._send_request")
    def test_post(self,mock_send_request,dhan_http):
        endpoint = "/endpoint"
        payload = {"key": "value"}
        dhan_http.post(endpoint,payload)
        mock_send_request.assert_called_once_with(DhanHTTP.HttpMethods.POST, endpoint, payload)
