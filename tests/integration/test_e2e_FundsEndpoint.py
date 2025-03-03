import json
import os
from pprint import pprint

import pytest
from dhanhq.constant import ExchangeSegment, PositionType, ProductType, TransactionType


class TestE2E_FundsEndpoint:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get_fund_limits.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_fund_limits(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.fundsEndpoint.get_fund_limits()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/margin_calculator.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_margin_calculator(self, expected_dict, dhanhq_fixture):
        endpoint = dhanhq_fixture.fundsEndpoint
        actual_response = endpoint.compute_margin_info("security_id", ExchangeSegment.NSE_EQ,
                                                       TransactionType.BUY, 100, ProductType.CNC, 99.99)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']
