from unittest.mock import Mock, patch


class TestDhanhq_orderupdate:

    @patch("builtins.print")
    def test_order_update_with_no_callback(
        self, mock_print, orderUpdate_fixture
    ):
        order_data = {
            "Type": "order_alert",
            "Data": dict(orderNo=123, status="order_status"),
        }

        # With order No
        orderUpdate_fixture.handle_order_update(order_data)

        # No order No
        order_data["Data"].pop("orderNo")
        orderUpdate_fixture.handle_order_update(order_data)

        # Unknown order type
        order_data["Type"] = "unknown"
        orderUpdate_fixture.handle_order_update(order_data)

        assert mock_print.call_count == 3

    def test_order_update_with_callback(self, orderUpdate_fixture):
        order_data = dict(Type="order_alert")

        mock_cb = Mock(spec=lambda _: None)

        orderUpdate_fixture.on_update = mock_cb

        orderUpdate_fixture.handle_order_update(order_data)

        mock_cb.assert_called_once_with(order_data)
