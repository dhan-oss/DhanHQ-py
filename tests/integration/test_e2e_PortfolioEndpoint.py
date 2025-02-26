import json
import os
from pprint import pprint

import pytest
from dhanhq.constants import ExchangeSegment, PositionType, ProductType, TransactionType


class TestE2E_PortfolioEndpoint:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-current-holdings.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_holdings(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.portfolioEndpoint.get_holdings()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get_positions.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_positions(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.portfolioEndpoint.get_positions()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/convert_position.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_convert_position(self, expected_dict, dhanhq_fixture):
        endpoint = dhanhq_fixture.portfolioEndpoint
        actual_response = endpoint.convert_position(ProductType.CNC, ExchangeSegment.NSE_EQ, PositionType.LONG,
                                                    "security_id", -99, ProductType.INTRADAY)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']
