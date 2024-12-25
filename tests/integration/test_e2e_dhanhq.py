import json
import os
from pprint import pprint

import pytest

from dhanhq import DhanContext, dhanhq
# from tests.conftest import api_access_token_fixture

@pytest.fixture
def dhanhq_obj(api_client_id_fixture, api_access_token_fixture):
    dhan_context = DhanContext(api_client_id_fixture, api_access_token_fixture)
    return dhanhq(dhan_context)

class TestE2E_Dhanhq_Orders:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-current-orders-list.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_order_list(self, expected_dict, dhanhq_obj):
        actual_response = dhanhq_obj.get_order_list()
        # pprint(actual_response)
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

class TestE2E_Dhanhq_Portfolio:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-current-holdings.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_holdings(self, expected_dict, dhanhq_obj):
        actual_response = dhanhq_obj.get_holdings()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']