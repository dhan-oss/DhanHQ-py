import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, Mock, patch


class TestDhanhq_orderupdate:

    def test_connection_keeps_token_out_of_stdout(self, orderUpdate_fixture, capsys):
        message = {"Type": "order_alert", "Data": {"orderNo": "123", "status": "TRADED"}}
        websocket = MagicMock()
        websocket.send = AsyncMock()
        websocket.__aiter__.return_value = [json.dumps(message)]
        connection = MagicMock()
        connection.__aenter__.return_value = websocket
        orderUpdate_fixture.on_update = Mock()

        with patch("dhanhq.orderupdate.websockets.connect", return_value=connection):
            asyncio.run(orderUpdate_fixture.connect_order_update())

        auth = json.loads(websocket.send.call_args.args[0])
        assert auth["LoginReq"]["Token"] == orderUpdate_fixture.access_token
        orderUpdate_fixture.on_update.assert_called_once_with(message)
        captured = capsys.readouterr()
        assert orderUpdate_fixture.access_token not in captured.out + captured.err

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
