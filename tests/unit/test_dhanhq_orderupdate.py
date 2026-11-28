import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
import websockets

from dhanhq import DhanContext, OrderUpdate


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

    def test_init_defaults_and_options(self):
        context = DhanContext("test_client", "test_token")
        on_connect_cb = Mock()
        on_close_cb = Mock()
        on_error_cb = Mock()
        on_update_cb = Mock()

        order_update = OrderUpdate(
            context,
            on_connect=on_connect_cb,
            on_close=on_close_cb,
            on_error=on_error_cb,
            on_update=on_update_cb,
        )

        assert order_update.client_id == "test_client"
        assert order_update.access_token == "test_token"
        assert order_update.ws is None
        assert order_update._running is False
        assert order_update._connecting is False
        assert order_update.on_connect == on_connect_cb
        assert order_update.on_close == on_close_cb
        assert order_update.on_error == on_error_cb
        assert order_update.on_update == on_update_cb

    def test_is_ws_closed(self, orderUpdate_fixture):
        # ws is None
        assert orderUpdate_fixture._is_ws_closed(None) is True

        # ws is open
        mock_ws = MagicMock()
        mock_ws.closed = False
        mock_ws.state = None
        assert orderUpdate_fixture._is_ws_closed(mock_ws) is False

        # ws is closed via closed attribute
        mock_ws.closed = True
        assert orderUpdate_fixture._is_ws_closed(mock_ws) is True

        # ws raises on access
        broken_ws = MagicMock()
        type(broken_ws).closed = property(lambda self: 1 / 0)
        assert orderUpdate_fixture._is_ws_closed(broken_ws) is True

    @pytest.mark.asyncio
    @patch("dhanhq.orderupdate.websockets.connect", new_callable=AsyncMock)
    async def test_connect_success_and_guard(self, mock_ws_connect, orderUpdate_fixture):
        mock_ws = AsyncMock()
        mock_ws.closed = False
        mock_ws.state = None
        mock_ws_connect.return_value = mock_ws

        connect_cb = Mock()
        orderUpdate_fixture.on_connect = connect_cb

        await orderUpdate_fixture.connect()

        assert orderUpdate_fixture.ws == mock_ws
        mock_ws_connect.assert_called_once_with(orderUpdate_fixture.order_feed_wss)
        mock_ws.send.assert_called_once()
        sent_data = json.loads(mock_ws.send.call_args[0][0])
        assert sent_data["LoginReq"]["ClientId"] == "test_client_id"
        assert sent_data["LoginReq"]["Token"] == "test_access_token"
        assert sent_data["LoginReq"]["MsgCode"] == 42
        connect_cb.assert_called_once_with(orderUpdate_fixture)

        # Calling connect again should be a no-op because ws is active
        await orderUpdate_fixture.connect()
        assert mock_ws_connect.call_count == 1

    @pytest.mark.asyncio
    async def test_disconnect_lifecycle(self, orderUpdate_fixture):
        mock_ws = AsyncMock()
        mock_ws.closed = False
        orderUpdate_fixture.ws = mock_ws
        orderUpdate_fixture._running = True

        close_cb = Mock()
        orderUpdate_fixture.on_close = close_cb

        await orderUpdate_fixture.disconnect()

        assert orderUpdate_fixture.ws is None
        assert orderUpdate_fixture._running is False
        mock_ws.close.assert_awaited_once()
        close_cb.assert_called_once_with(orderUpdate_fixture)

    def test_close_connection_stopped_loop(self, orderUpdate_fixture):
        mock_ws = AsyncMock()
        mock_ws.closed = False
        orderUpdate_fixture.ws = mock_ws
        orderUpdate_fixture._running = True

        orderUpdate_fixture.close_connection()

        assert orderUpdate_fixture.ws is None
        assert orderUpdate_fixture._running is False
        mock_ws.close.assert_awaited_once()

    def test_close_connection_running_loop(self, orderUpdate_fixture):
        mock_ws = AsyncMock()
        mock_ws.closed = False
        orderUpdate_fixture.ws = mock_ws
        orderUpdate_fixture._running = True

        with patch("asyncio.run_coroutine_threadsafe") as mock_threadsafe:
            mock_future = Mock()
            mock_future.result.return_value = None

            def fake_threadsafe(coro, loop):
                coro.close()
                return mock_future

            mock_threadsafe.side_effect = fake_threadsafe

            orderUpdate_fixture.loop = MagicMock()
            orderUpdate_fixture.loop.is_running.return_value = True

            orderUpdate_fixture.close_connection()

            assert orderUpdate_fixture._running is False
            mock_threadsafe.assert_called_once()

    def test_close_connection_closed_loop(self, orderUpdate_fixture):
        orderUpdate_fixture.loop = MagicMock()
        orderUpdate_fixture.loop.is_running.return_value = False
        orderUpdate_fixture.loop.is_closed.return_value = True

        # Should return safely without raising
        orderUpdate_fixture.close_connection()
        assert orderUpdate_fixture._running is False

    def test_run_handles_keyboard_interrupt(self, orderUpdate_fixture):
        with patch.object(orderUpdate_fixture, "_run_async", side_effect=KeyboardInterrupt):
            with patch.object(orderUpdate_fixture, "close_connection") as mock_close:
                orderUpdate_fixture.run()
                mock_close.assert_called_once()

    @patch("threading.Thread")
    def test_start_spawns_daemon_thread(self, mock_thread_class, orderUpdate_fixture):
        mock_thread = Mock()
        mock_thread_class.return_value = mock_thread

        result = orderUpdate_fixture.start()

        mock_thread_class.assert_called_once_with(target=orderUpdate_fixture.run, daemon=True)
        mock_thread.start.assert_called_once()
        assert result == mock_thread

    @pytest.mark.asyncio
    async def test_process_next_message_success(self, orderUpdate_fixture):
        mock_ws = AsyncMock()
        payload = json.dumps({"Type": "order_alert", "Data": {"orderNo": "999", "status": "TRADED"}})
        mock_ws.recv.return_value = payload

        with patch.object(orderUpdate_fixture, "handle_order_update") as mock_handle:
            await orderUpdate_fixture._process_next_message(mock_ws)
            mock_handle.assert_called_once_with(
                {"Type": "order_alert", "Data": {"orderNo": "999", "status": "TRADED"}}
            )

    @pytest.mark.asyncio
    async def test_process_next_message_timeout(self, orderUpdate_fixture):
        mock_ws = AsyncMock()
        mock_ws.recv.side_effect = asyncio.TimeoutError()

        with patch.object(orderUpdate_fixture, "handle_order_update") as mock_handle:
            await orderUpdate_fixture._process_next_message(mock_ws)
            mock_handle.assert_not_called()

    @pytest.mark.asyncio
    async def test_handle_error_callbacks(self, orderUpdate_fixture):
        mock_error = ValueError("test error")

        # With on_error callback
        error_cb = Mock()
        orderUpdate_fixture.on_error = error_cb
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            await orderUpdate_fixture._handle_error(mock_error)
            error_cb.assert_called_once_with(orderUpdate_fixture, mock_error)
            mock_sleep.assert_awaited_once_with(1)

        # Without on_error callback (fallback to print)
        orderUpdate_fixture.on_error = None
        with patch("builtins.print") as mock_print, patch("asyncio.sleep", new_callable=AsyncMock):
            await orderUpdate_fixture._handle_error(mock_error)
            assert any("test error" in str(arg) for call in mock_print.call_args_list for arg in call[0])

    @pytest.mark.asyncio
    async def test_connect_order_update_backward_compatibility(self, orderUpdate_fixture):
        with patch.object(orderUpdate_fixture, "_run_async", new_callable=AsyncMock) as mock_run_async:
            await orderUpdate_fixture.connect_order_update()
            assert orderUpdate_fixture._running is True
            mock_run_async.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_disconnect_exception_logged(self, orderUpdate_fixture):
        mock_ws = AsyncMock()
        mock_ws.close.side_effect = Exception("close failure")
        orderUpdate_fixture.ws = mock_ws
        orderUpdate_fixture._running = True

        with patch("builtins.print") as mock_print:
            await orderUpdate_fixture.disconnect()
            assert orderUpdate_fixture.ws is None
            assert any("close failure" in str(arg) for call in mock_print.call_args_list for arg in call[0])

    @pytest.mark.asyncio
    async def test_close_connection_from_same_loop(self, orderUpdate_fixture):
        orderUpdate_fixture.loop = asyncio.get_running_loop()
        with patch.object(orderUpdate_fixture, "disconnect", new_callable=AsyncMock) as mock_disconnect:
            orderUpdate_fixture.close_connection()
            # Allow the created task to run
            await asyncio.sleep(0.01)
            mock_disconnect.assert_awaited_once()

    def test_run_recreates_closed_loop(self, orderUpdate_fixture):
        orderUpdate_fixture.loop.close()
        assert orderUpdate_fixture.loop.is_closed() is True

        with patch.object(orderUpdate_fixture, "_run_async", new_callable=AsyncMock) as mock_run_async:
            orderUpdate_fixture.run()
            assert orderUpdate_fixture.loop.is_closed() is False
            mock_run_async.assert_awaited_once()

    def test_connect_to_dhan_websocket_sync_catches_exception(self, orderUpdate_fixture):
        with patch.object(orderUpdate_fixture, "run", side_effect=RuntimeError("sync crash")):
            with patch("builtins.print") as mock_print:
                orderUpdate_fixture.connect_to_dhan_websocket_sync()
                assert any("sync crash" in str(arg) for call in mock_print.call_args_list for arg in call[0])

    @pytest.mark.asyncio
    async def test_run_async_reconnects_on_connection_closed(self, orderUpdate_fixture):
        mock_ws = AsyncMock()
        mock_ws.recv.side_effect = [
            json.dumps({"Type": "order_alert", "Data": {"orderNo": "1"}}),
            websockets.ConnectionClosed(None, None),
        ]

        connect_calls = 0

        async def fake_connect():
            nonlocal connect_calls
            connect_calls += 1
            orderUpdate_fixture.ws = mock_ws
            if connect_calls > 1:
                orderUpdate_fixture._running = False

        with patch.object(orderUpdate_fixture, "connect", side_effect=fake_connect):
            with patch("asyncio.sleep", new_callable=AsyncMock):
                orderUpdate_fixture._running = True
                await orderUpdate_fixture._run_async()
                assert connect_calls >= 2
