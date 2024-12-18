# import sys
import pytest
import requests
from json import loads as json_loads, dumps as json_dumps
from unittest.mock import patch  # for mocking requests

# print(sys.path)
from dhanhq.dhanhq import dhanhq

@pytest.fixture
def dhanhq_obj():
    return dhanhq("test_client_id", "test_access_token")

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

class TestDhanhq_Private_Constructor:
    def test_init_success(self, dhanhq_obj):
        assert dhanhq_obj.client_id == "test_client_id"
        assert dhanhq_obj.access_token == "test_access_token"
        assert dhanhq_obj.base_url == "https://api.dhan.co/v2"
        assert dhanhq_obj.timeout == 60
        assert dhanhq_obj.header["access-token"] == "test_access_token"

class TestDhanhq_Private_ParseResponse:
    def test_parse_response_success_with_status_code_200(self, dhanhq_obj, mock_success_response):
        parsed_response = dhanhq_obj._parse_response(mock_success_response)
        assert parsed_response["status"] == "success"
        assert parsed_response["remarks"] == ""
        assert parsed_response["data"] == {"data": "some data"}

    def test_parse_response_error_with_status_code_400(self, dhanhq_obj, mock_failure_response):
        parsed_response = dhanhq_obj._parse_response(mock_failure_response)
        assert parsed_response["status"] == "failure"
        assert parsed_response["remarks"]["error_type"] == "test_error"
        assert parsed_response["remarks"]["error_message"] == "test message"

class TestDhanhq_Private_GetRequest:
    @patch("requests.Session.get")
    def test_get_request_success(self, mock_session_get, dhanhq_obj, mock_success_response):
        endpoint = '/resource/123'
        mock_session_get.return_value = mock_success_response
        response = dhanhq_obj._get_request(endpoint)
        mock_session_get.assert_called_once()
        # args, _ = mock_session_get.call_args
        assert mock_session_get.call_args[0][0] == dhanhq_obj.base_url+endpoint # Check 1st arg to call having endpoint
        assert response["status"] == "success"

    @patch("requests.Session.get")
    def test_get_request_exception(self, mock_session_get, dhanhq_obj):
        endpoint = '/resource/123'
        mock_session_get.side_effect = Exception("Test exception")
        response = dhanhq_obj._get_request(endpoint)
        mock_session_get.assert_called_once()
        assert mock_session_get.call_args[0][0] == dhanhq_obj.base_url+endpoint
        assert response["status"] == "failure"
        assert "Test exception" in response["remarks"]

class TestDhanhq_Private_DeleteRequest:
    @patch("requests.Session.delete")
    def test_get_request_success(self, mock_session_delete, dhanhq_obj, mock_success_response):
        endpoint = "/resource/123"
        mock_session_delete.return_value = mock_success_response
        response = dhanhq_obj._delete_request(endpoint)
        mock_session_delete.assert_called_once()
        assert mock_session_delete.call_args[0][0] == dhanhq_obj.base_url+endpoint
        assert response["status"] == "success"

class TestDhanhq_Private_PostRequest:
    @patch("requests.Session.post")
    def test_get_request_success(self, mock_session_post, dhanhq_obj, mock_success_response):
        endpoint = "/resource"
        payload = {"one": "1","two":"2"}
        mock_session_post.return_value = mock_success_response
        response = dhanhq_obj._post_request(endpoint,payload)
        mock_session_post.assert_called_once() #_with(endpoint, json_dumps(payload))
        assert mock_session_post.call_args[0][0] == dhanhq_obj.base_url+endpoint
        assert mock_session_post.call_args[1]['data'] == json_dumps(payload)
        assert response["status"] == "success"

class TestDhanhq_Orders:
    @patch("dhanhq.dhanhq._get_request") #patching the helper here
    def test_get_order_list_success(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_order_list()
        mock_get_request.assert_called_once_with('/orders')

    @patch("dhanhq.dhanhq._get_request") #patching the helper here
    def test_get_order_by_id(self, mock_get_request, dhanhq_obj):
        order_id = "12345"
        response = dhanhq_obj.get_order_by_id(order_id)
        mock_get_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.dhanhq._get_request") #patching the helper here
    def test_get_order_by_correlationID(self, mock_get_request, dhanhq_obj):
        correlationID = "12345"
        response = dhanhq_obj.get_order_by_correlationID(correlationID)
        mock_get_request.assert_called_once_with(f'/orders/external/{correlationID}')

    @patch("dhanhq.dhanhq._delete_request")
    def test_cancel_order_success(self, mock_delete_request, dhanhq_obj):
        order_id = "12345"
        dhanhq_obj.cancel_order(order_id)
        mock_delete_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.dhanhq._post_request")
    def test_place_order_success(self,mock_post_request,dhanhq_obj):
        endpoint = '/orders';
        security_id = 1
        exchange_segment = "exchange_segment"
        transaction_type = "transaction_type"
        quantity =100
        order_type = "order_type"
        product_type = "product_type"
        price = 123
        dhanhq_obj.place_order(security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity='DAY', amo_time='OPEN',
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None)
        mock_post_request.assert_called_once()
        assert mock_post_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhanhq._post_request")
    def test_place_slice_order_success(self,mock_post_request,dhanhq_obj):
        endpoint = '/orders/slicing';
        security_id = 1
        exchange_segment = "exchange_segment"
        transaction_type = "transaction_type"
        quantity =100
        order_type = "order_type"
        product_type = "product_type"
        price = 123
        dhanhq_obj.place_slice_order(security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity='DAY', amo_time='OPEN',
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None)
        mock_post_request.assert_called_once()
        assert mock_post_request.call_args[0][0] == endpoint
