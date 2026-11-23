import asyncio
import json
import struct
from unittest.mock import AsyncMock, MagicMock

import pytest
from dhanhq import DhanContext, CASFeed

# Packets captured from the live CAS feed on 2026-11-23.
# HDFC Bank (NSE_EQ 1333) CAS packet.
CAS_1333 = bytes.fromhex(
    '098000013505000033734c44be654e005b153b00413b03003ff500003a000e0066865244664646449b0000000100'
    '0000030001000080524400e046446a0000002c01000001000300000052440080474408000000610600000200060000'
    'c050440000484422821b004e622300b802cb000ad723bc0ad723bc61d2000066664c44')
# Indicative index values: NIFTY 50 (13) and NIFTY BANK (25), sent concatenated in one message.
INDEX_13 = bytes.fromhex('0a0c00000d0000004d0bc646')
INDEX_25 = bytes.fromhex('0a0c0000190000005a797447')


class TestCASFeed:
    @pytest.fixture
    def feed(self):
        return CASFeed(DhanContext("client_id", "access_token"), [(CASFeed.NSE, "1333"), ("IDX_I", "13")])

    def test_cas_packet(self, feed):
        data = feed.process_data(CAS_1333)
        assert data["type"] == "CAS"
        assert data["exchange_segment"] == 1
        assert data["security_id"] == 1333
        assert data["IEP"] == "817.80"
        assert data["total_buy_quantity"] == 5137854
        assert data["total_sell_quantity"] == 3872091
        assert data["imbalance_quantity"] == 53857
        assert data["reference_price"] == "817.60"
        assert len(data["depth"]) == 5
        assert data["depth"][0] == {"bid_quantity": 211777, "ask_quantity": 62783, "bid_orders": 58,
                                    "ask_orders": 14, "bid_price": "842.10", "ask_price": "793.10"}

    def test_index_value_packet(self, feed):
        data = feed.process_data(INDEX_13)
        assert data == {"type": "CAS Index", "exchange_segment": 0, "security_id": 13,
                        "indicative_value": "25349.65"}

    def test_concatenated_packets(self, feed):
        data = feed.process_data(INDEX_25 + INDEX_13 + CAS_1333)
        assert [p["type"] for p in data] == ["CAS Index", "CAS Index", "CAS"]
        assert [p["security_id"] for p in data] == [25, 13, 1333]

    def test_documented_index_name_packet(self, feed):
        packet = struct.pack('<HBB21sd', 33, 11, 0, b'NIFTY 50', 25349.65)
        data = feed.process_data(packet)
        assert data["type"] == "CAS Index"
        assert data["index_name"] == "NIFTY 50"
        assert data["indicative_value"] == "25349.65"

    def test_disconnect_packet(self, feed):
        feed.on_close = MagicMock()
        packet = struct.pack('<BHBIH', 50, 10, 1, 1333, 807)
        data = feed.process_data(packet)
        assert data["type"] == "Disconnect"
        assert data["error_code"] == 807
        assert data["message"] == "Access token is expired."
        feed.on_close.assert_called_once_with(feed)

    def test_truncated_packet_is_ignored(self, feed):
        data = feed.process_data(INDEX_13 + CAS_1333[:60])
        assert data["type"] == "CAS Index"

    def test_unknown_packet_stops_parsing(self, feed):
        assert feed.process_data(b'\x63' * 16) == []

    def test_subscription_messages(self, feed):
        messages = feed.create_subscription_messages(CASFeed.Subscribe, feed.instruments)
        assert messages == [{
            "RequestCode": 23,
            "InstrumentCount": 2,
            "InstrumentList": [{"ExchangeSegment": "NSE_EQ", "SecurityId": "1333"},
                               {"ExchangeSegment": "IDX_I", "SecurityId": "13"}]
        }]

    def test_subscription_messages_are_batched(self, feed):
        instruments = [(CASFeed.NSE, str(i)) for i in range(250)]
        messages = feed.create_subscription_messages(CASFeed.Subscribe, instruments)
        assert [m["InstrumentCount"] for m in messages] == [100, 100, 50]

    def test_invalid_exchange_segment(self, feed):
        with pytest.raises(ValueError):
            feed.create_subscription_messages(CASFeed.Subscribe, [("FOO", "1")])
        with pytest.raises(ValueError):
            feed.create_subscription_messages(CASFeed.Subscribe, [(6, "1")])

    def test_connect_uses_version_2_url_and_subscribes(self, feed, monkeypatch):
        ws = MagicMock()
        ws.send = AsyncMock()
        connect = AsyncMock(return_value=ws)
        monkeypatch.setattr("dhanhq.cas_feed.websockets.connect", connect)
        feed.on_connect = MagicMock()
        feed.run_forever()
        url = connect.call_args[0][0]
        assert url == "wss://api-feed.dhan.co?version=2&token=access_token&clientId=client_id&authType=2"
        sent = json.loads(ws.send.call_args[0][0])
        assert sent["RequestCode"] == 23 and sent["InstrumentCount"] == 2
        feed.on_connect.assert_called_once_with(feed)

    def test_unsubscribe_sends_code_24(self, feed):
        feed.ws = MagicMock()
        feed.ws.closed = False
        feed.ws.send = AsyncMock()
        feed.unsubscribe_symbols([(CASFeed.NSE, "1333")])
        feed.loop.run_until_complete(asyncio.sleep(0.05))
        sent = json.loads(feed.ws.send.call_args[0][0])
        assert sent == {"RequestCode": 24, "InstrumentCount": 1,
                        "InstrumentList": [{"ExchangeSegment": "NSE_EQ", "SecurityId": "1333"}]}
        assert feed.instruments == [("IDX_I", "13")]

    def test_disconnect_sends_code_12(self, feed):
        feed.ws = MagicMock()
        feed.ws.send = AsyncMock()
        feed.ws.close = AsyncMock()
        feed.on_close = MagicMock()
        feed.close_connection()
        assert json.loads(feed.ws.send.call_args[0][0]) == {"RequestCode": 12}
        feed.ws.close.assert_awaited_once()
        feed.on_close.assert_called_once_with(feed)

    def test_close_from_another_thread_does_not_hang(self, feed, monkeypatch):
        """The server closes the socket on code 12; the recv loop must not stop before disconnect() finishes."""
        import time
        import websockets
        closed = asyncio.Event()

        async def recv():
            await closed.wait()
            raise websockets.ConnectionClosed(None, None)

        async def close():
            await asyncio.sleep(0.2)  # close handshake still in flight when recv() raises
            closed.set()
            await asyncio.sleep(0.2)

        ws = MagicMock()
        ws.closed = False
        ws.send = AsyncMock(side_effect=lambda m: closed.set() if json.loads(m)["RequestCode"] == 12 else None)
        ws.recv = recv
        ws.close = AsyncMock(side_effect=close)
        monkeypatch.setattr("dhanhq.cas_feed.websockets.connect", AsyncMock(return_value=ws))
        feed.on_close = MagicMock()
        thread = feed.start()
        time.sleep(0.2)
        feed.close_connection()
        thread.join(timeout=5)
        assert not thread.is_alive()
        ws.close.assert_awaited_once()
        feed.on_close.assert_called_once_with(feed)
