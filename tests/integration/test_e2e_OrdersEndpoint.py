import json
import os
from pprint import pprint

import pytest
from dhanhq.constant import ExchangeSegment, LegName, OrderType, ProductType, TransactionType, Validity


# from tests.conftest import api_access_token_fixture

class TestE2E_OrdersEndpoint:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-current-orders-list.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_orders(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.orderEndpoint.get_orders()
        # pprint(actual_response)
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-order_req-by-id.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_order_by_id(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.orderEndpoint.get_order_by_id("string")
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-order_req-by-correlation-id.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_order_by_correlation_id(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.orderEndpoint.get_order_by_id("string")
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/modify_pending_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_modify_order(self, expected_dict, dhanhq_fixture):
        endpoint = dhanhq_fixture.orderEndpoint
        actual_response = endpoint.modify_order("string", OrderType.LIMIT, LegName.ENTRY_LEG, 1, 11, 12.0, 1, Validity.DAY)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/cancel_given_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_cancel_order(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.orderEndpoint.cancel_order("string")
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/place_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_place_order(self, expected_dict, dhanhq_fixture):
        endpoint = dhanhq_fixture.orderEndpoint
        actual_response = endpoint.place_order("security_id", ExchangeSegment.NSE_EQ, TransactionType.BUY,
                                               100, OrderType.LIMIT, ProductType.CNC, 99.99, 0)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/place_slice_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_place_slice_order(self, expected_dict, dhanhq_fixture):
        endpoint = dhanhq_fixture.orderEndpoint
        actual_response = endpoint.place_slice_order("security_id", ExchangeSegment.NSE_EQ, TransactionType.BUY,
                                                     100, OrderType.LIMIT, ProductType.CNC, 99.99, 0)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

