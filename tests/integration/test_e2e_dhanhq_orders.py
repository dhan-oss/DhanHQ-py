import json
import os
from pprint import pprint

import pytest
from dhanhq import DhanCore
from dhanhq.constants.exchange_segment import ExchangeSegment
from dhanhq.constants.transaction_type import TransactionType


# from tests.conftest import api_access_token_fixture

class TestE2E_Dhanhq_Orders:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-current-orders-list.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_order_list(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_order_list()
        # pprint(actual_response)
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-order-by-id.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_order_by_id(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_order_by_id("string")
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-order-by-correlation-id.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_order_by_correlation_id(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_order_by_id("string")
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/modify_pending_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_modify_order(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.modify_order("string", DhanCore.LIMIT, "ENTRY_LEG", 1, 11, 12.0, 1, DhanCore.DAY)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/cancel_given_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_cancel_order(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.cancel_order("string")
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/place_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_place_order(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.place_order("security_id", ExchangeSegment.NSE_EQ, TransactionType.BUY,
                                                     100, DhanCore.LIMIT, DhanCore.CNC, 99.99, 0)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/place_slice_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_place_slice_order(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.place_slice_order("security_id", ExchangeSegment.NSE_EQ, TransactionType.BUY,
                                                           100, DhanCore.LIMIT, DhanCore.CNC, 99.99, 0)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

