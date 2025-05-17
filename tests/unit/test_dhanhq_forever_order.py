from json import dumps as json_dumps
from unittest.mock import patch

import pytest

from dhanhq import DhanContext
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhanhq import dhanhq


class TestDhanhq_ForeverOrder:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_forever(self,mock_read_request,dhanhq_obj):
        dhanhq_obj.get_forever()
        mock_read_request.assert_called_once_with('/forever/orders')

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_forever(self,mock_create_request, dhanhq_obj):
        endpoint = '/forever/orders'
        quantity = 100
        price = 108
        trigger_Price = 110
        dhanhq_obj.place_forever("security_id", "exchange_segment", "transaction_type",
                                 "product_type", "order_type", quantity, price, trigger_Price)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.put")
    def test_modify_forever(self, mock_update_request, dhanhq_obj):
        order_id = 123
        endpoint = f'/forever/orders/{order_id}'
        quantity = 100
        price = 108
        trigger_price = 110
        disclosed_quantity = 555
        dhanhq_obj.modify_forever(order_id, "order_flag", "order_type", "leg_name",
                                  quantity, price, trigger_price, disclosed_quantity,"validity")
        mock_update_request.assert_called_once()
        assert mock_update_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.delete")
    def test_cancel_forever(self, mock_delete_request, dhanhq_obj):
        order_id = "123"
        endpoint = f'/forever/orders/{order_id}'
        dhanhq_obj.cancel_forever(order_id)
        mock_delete_request.assert_called_once_with(endpoint)
