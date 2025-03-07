import json
import os
from pprint import pprint

import pytest
from dhanhq import dhanhq

class TestE2E_Dhanhq_Portfolio:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-current-holdings.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_holdings(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_holdings()
        pprint("actual_response = " + actual_response)
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get_positions.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_positions(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_positions()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/convert_position.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_convert_position(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.convert_position(dhanhq.CNC, dhanhq.NSE, "LONG", "security_id", -99, dhanhq.INTRA)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

class TestE2E_Dhanhq_Funds:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get_fund_limits.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_fund_limits(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_fund_limits()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/margin_calculator.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_margin_calculator(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.margin_calculator("security_id", dhanhq.NSE, dhanhq.BUY, 100, dhanhq.CNC, 99.99)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']
