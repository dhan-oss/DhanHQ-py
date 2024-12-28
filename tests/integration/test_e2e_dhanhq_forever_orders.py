import json
import os
from pprint import pprint

import pytest
from dhanhq import dhanhq

# from tests.conftest import api_access_token_fixture

class TestE2E_Dhanhq_Forever_Orders:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-forever-orders-list.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_order_list(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_forever()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/modify_pending_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_modify_order(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.modify_forever("order_id", "SINGLE", dhanhq.LIMIT, "TARGET_LEG",
                                                        100, 99.99, 99.99, 100,dhanhq.DAY)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/cancel_given_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_cancel_forever(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.cancel_forever("string")
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/place_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_place_forever(self, expected_dict, dhanhq_fixture):

        actual_response = dhanhq_fixture.place_forever("security_id", dhanhq.NSE, dhanhq.BUY, dhanhq.CNC,
                                                       dhanhq.LIMIT,100, 99.99, 99.99)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']
