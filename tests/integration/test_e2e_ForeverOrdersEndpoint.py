import json
import os
from pprint import pprint

import pytest
from dhanhq.constant import ExchangeSegment, LegName, OrderFlag, OrderType, ProductType, TransactionType, Validity
from dhanhq.dto import ModifyForeverOrderRequest, NewForeverOrderRequest


# from tests.conftest import api_access_token_fixture

class TestE2E_ForeverOrdersEndpoint:
    json_file_path = os.path.join(os.path.dirname(__file__), '../data/get-forever-orders-list.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_get_order_list(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.foreverOrderEndpoint.get_forever_orders()
        assert actual_response == []

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/modify_pending_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_modify_order(self, expected_dict, dhanhq_fixture):
        endpoint = dhanhq_fixture.foreverOrderEndpoint
        request = ModifyForeverOrderRequest(order_id="111", order_flag=OrderFlag.SINGLE,
                                            order_type=OrderType.LIMIT, leg_name=LegName.TARGET_LEG,
                                            quantity=100, price=99.99, trigger_price=99.99,
                                            disclosed_quantity=100, validity=Validity.DAY)
        actual_response = endpoint.modify_forever_order(request)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/cancel_given_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_cancel_forever(self, expected_dict, dhanhq_fixture):
        actual_response = dhanhq_fixture.foreverOrderEndpoint.cancel_pending_forever_order("string")
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']

    json_file_path = os.path.join(os.path.dirname(__file__), '../data/place_order.json')
    @pytest.mark.parametrize("expected_dict", [json.load(open(json_file_path))])
    def test_place_forever(self, expected_dict, dhanhq_fixture):
        endpoint = dhanhq_fixture.foreverOrderEndpoint
        request = NewForeverOrderRequest(security_id="123", exchange_segment=ExchangeSegment.NSE_EQ,
                                         transaction_type=TransactionType.BUY, product_type=ProductType.CNC,
                                         order_type=OrderType.LIMIT, quantity=100, price=99.99, trigger_price=99.99)
        actual_response = endpoint.place_forever_order(request)
        # assert actual_response['status'] == expected_dict['status']
        # assert actual_response['remarks'] == expected_dict['remarks']
        # assert actual_response['data'] == expected_dict['data']
