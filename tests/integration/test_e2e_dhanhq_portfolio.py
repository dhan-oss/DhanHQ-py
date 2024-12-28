import json
import os
from pprint import pprint

import pytest

class TestE2E_Dhanhq_Portfolio:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-current-holdings.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_holdings(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_holdings()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']