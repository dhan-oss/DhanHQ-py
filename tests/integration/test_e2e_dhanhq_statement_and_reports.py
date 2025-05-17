import json
import os
from datetime import date
from pprint import pprint

import pytest


class TestE2E_Dhanhq_StatementsAndReports:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get_all_trades.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_trade_book_without_orderid(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_trade_book()
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get_trade_book_by_orderid.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_trade_book_by_orderid(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.get_trade_book("order_id")
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get_trade_history.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_trade_history(self, expected_dict, dhanhq_fixture):
        str_today = date.today().strftime('%Y-%m-%d')
        actual_response = dhanhq_fixture.get_trade_history(str_today,str_today,page_number=0)
        # pprint(actual_response)
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']


    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get_ledger_report.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_ledger_report(self, expected_dict, dhanhq_fixture):
        str_today = date.today().strftime('%Y-%m-%d')
        actual_response = dhanhq_fixture.ledger_report(str_today, str_today)
        # pprint(actual_response)
        assert actual_response['status'] == expected_dict['status']
        assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

