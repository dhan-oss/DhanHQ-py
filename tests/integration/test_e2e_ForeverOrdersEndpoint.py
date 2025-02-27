import json
import os
from pprint import pprint

import pytest
from dhanhq.constant import ExchangeSegment, LegName, OrderFlag, OrderType, ProductType, TransactionType, Validity


# from tests.conftest import api_access_token_fixture

class TestE2E_ForeverOrdersEndpoint:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-forever-orders-list.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_order_list(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.foreverOrderEndpoint.get_forever()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/modify_pending_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_modify_order(self, expected_dict, dhanhq_fixture):
        endpoint = dhanhq_fixture.foreverOrderEndpoint
        actual_response = endpoint.modify_forever("order_id", OrderFlag.SINGLE, OrderType.LIMIT, LegName.TARGET_LEG,
                                                  100, 99.99, 99.99, 100, Validity.DAY)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/cancel_given_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_cancel_forever(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.foreverOrderEndpoint.cancel_forever("string")
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/place_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_place_forever(self, expected_dict, dhanhq_fixture):
        endpoint = dhanhq_fixture.foreverOrderEndpoint
        actual_response = endpoint.place_forever("security_id", ExchangeSegment.NSE_EQ,
                                                 TransactionType.BUY, ProductType.CNC,
                                                 OrderType.LIMIT, 100, 99.99, 99.99)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']
