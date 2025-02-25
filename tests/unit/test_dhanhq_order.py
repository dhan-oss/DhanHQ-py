from json import dumps as json_dumps
from unittest.mock import patch

import pytest

from dhanhq import DhanContext
from dhanhq.constants.amo_time import AMOTime
from dhanhq.constants.exchange_segment import ExchangeSegment
from dhanhq.constants.leg_name import LegName
from dhanhq.constants.order_type import OrderType
from dhanhq.constants.product_type import ProductType
from dhanhq.constants.transaction_type import TransactionType
from dhanhq.constants.validity import Validity
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhancore import DhanCore


class TestDhanhq_Orders:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_order_list_success(self, mock_read_request, dhanhq_obj):
        dhanhq_obj.get_order_list()
        mock_read_request.assert_called_once_with('/orders')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_order_by_id(self, mock_read_request, dhanhq_obj):
        order_id = "12345"
        dhanhq_obj.get_order_by_id(order_id)
        mock_read_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_order_by_correlation_id(self, mock_read_request, dhanhq_obj):
        correlation_id = "12345"
        dhanhq_obj.get_order_by_correlationID(correlation_id)
        mock_read_request.assert_called_once_with(f'/orders/external/{correlation_id}')

    @patch("dhanhq.dhan_http.DhanHTTP.delete")
    def test_cancel_order_success(self, mock_delete_request, dhanhq_obj):
        order_id = "12345"
        dhanhq_obj.cancel_order(order_id)
        mock_delete_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_order_success(self,mock_create_request,dhanhq_obj):
        endpoint = '/orders'
        security_id = 1
        exchange_segment = ExchangeSegment.NSE_EQ
        transaction_type = TransactionType.BUY
        quantity =100
        order_type = OrderType.MARKET
        product_type = ProductType.CNC
        price = 123
        dhanhq_obj.place_order(security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity=Validity.DAY, amo_time=AMOTime.OPEN,
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_slice_order_success(self,mock_create_request,dhanhq_obj):
        endpoint = '/orders/slicing'
        security_id = 1
        exchange_segment = ExchangeSegment.NSE_EQ
        transaction_type = TransactionType.BUY
        quantity =100
        order_type = OrderType.MARKET
        product_type = ProductType.CNC
        price = 123
        dhanhq_obj.place_slice_order(security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity=Validity.DAY, amo_time=AMOTime.OPEN,
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.put")
    def test_modify_order_success(self,mock_update_request,dhanhq_obj):
        order_id = 123
        endpoint = f'/orders/{order_id}'
        quantity = 100
        price = 99
        trigger_price = 100
        dhanhq_obj.modify_order(order_id, OrderType.STOP_LOSS, LegName.STOP_LOSS_LEG, quantity, price,
                                trigger_price, trigger_price, Validity.IOC)
        mock_update_request.assert_called_once()
        assert mock_update_request.call_args[0][0] == endpoint

