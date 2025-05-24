from json import dumps as json_dumps
from unittest.mock import patch
import pytest
from dhanhq import DhanContext
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhanhq import dhanhq


class TestDhanhq_SuperOrder:

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_super_order_list(self, mock_get_request, dhanhq_obj):
        dhanhq_obj.get_super_order_list()
        mock_get_request.assert_called_once_with('/super/orders')

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_super_order_valid_buy(self, mock_post_request, dhanhq_obj):
        endpoint = '/super/orders'
        dhanhq_obj.place_super_order(
            security_id="SEC123",
            exchange_segment="NSE",
            transaction_type="BUY",
            quantity=10,
            order_type="LIMIT",
            product_type="INTRA",
            price=100,
            targetPrice=110,
            stopLossPrice=90,
            trailingJump=1.5,
            tag="TAG123"
        )
        mock_post_request.assert_called_once()
        assert mock_post_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_super_order_invalid_legs(self, mock_post_request, dhanhq_obj):
        with pytest.raises(ValueError, match="All legs .* must be provided"):
            dhanhq_obj.place_super_order(
                security_id="SEC123",
                exchange_segment="NSE",
                transaction_type="BUY",
                quantity=10,
                order_type="LIMIT",
                product_type="INTRA",
                price=0,
                targetPrice=0,
                stopLossPrice=0,
                trailingJump=1.5,
                tag=""
            )

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_super_order_invalid_buy_logic(self, mock_post_request, dhanhq_obj):
        with pytest.raises(ValueError, match="For BUY: targetPrice must be > price"):
            dhanhq_obj.place_super_order(
                security_id="SEC123",
                exchange_segment="NSE",
                transaction_type="BUY",
                quantity=10,
                order_type="LIMIT",
                product_type="INTRA",
                price=100,
                targetPrice=95,
                stopLossPrice=105,
                trailingJump=1.5,
                tag=""
            )

    @patch("dhanhq.dhan_http.DhanHTTP.put")
    def test_modify_super_order_entry_leg(self, mock_put_request, dhanhq_obj):
        order_id = "ORD001"
        dhanhq_obj.modify_super_order(
            order_id=order_id,
            order_type="LIMIT",
            leg_name="ENTRY_LEG",
            quantity=10,
            price=100,
            targetPrice=110,
            stopLossPrice=90,
            trailingJump=1
        )
        mock_put_request.assert_called_once_with(
            f"/super/orders/{order_id}",
            {
                "orderId": order_id,
                "orderType": "LIMIT",
                "legName": "ENTRY_LEG",
                "quantity": 10,
                "price": 100.0,
                "targetPrice": 110.0,
                "stopLossPrice": 90.0,
                "trailingJump": 1.0
            }
        )

    @patch("dhanhq.dhan_http.DhanHTTP.delete")
    def test_cancel_super_order(self, mock_delete_request, dhanhq_obj):
        order_id = "ORD001"
        leg = "TARGET_LEG"
        endpoint = f"/super/orders/{order_id}/{leg}"
        dhanhq_obj.cancel_super_order(order_id, leg)
        mock_delete_request.assert_called_once_with(endpoint)
