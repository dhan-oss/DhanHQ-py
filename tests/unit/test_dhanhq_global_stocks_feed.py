import struct
from unittest.mock import MagicMock

import pytest
from dhanhq import DhanContext, GlobalStocksFeed

# Packets captured from the live Global Stocks feed (LCTX, security ID 10006001).
TRADE = bytes.fromhex('0ef1ad9800f1ad98001b013bdf6f3f825d000041eac76afa9cc76a')
PREV_CLOSE = bytes.fromhex('0ef1ad9800f1ad98000f20ea95723f')
CIRCUIT_LIMIT = bytes.fromhex('0ef1ad9800f1ad98001321e6ae9d3f07ce293f')
WEEK_52 = bytes.fromhex('0ef1ad9800f1ad980013248fc205406ade613f')
OHLC = bytes.fromhex('0ef1ad9800f1ad98001b03f4fd743f3333733fe10b733f7b146e3f')
# Error packet returned when connecting with an invalid token.
ERROR_807 = bytes.fromhex('0000000000000000000d322703')


def header(msg_length, msg_code, scrip_id=10006001):
    return struct.pack('<BiiBB', 14, scrip_id, scrip_id, msg_length, msg_code)


class TestGlobalStocksFeed:
    @pytest.fixture
    def feed(self):
        return GlobalStocksFeed(DhanContext("client_id", "access_token"), [(GlobalStocksFeed.INX_EQ, "10006001")])

    def test_trade(self, feed):
        data = feed.process_data(TRADE)
        assert data["type"] == "Trade"
        assert data["exchange_segment"] == 14
        assert data["security_id"] == 10006001
        assert data["LTP"] == "0.94"
        assert data["volume"] == 23938
        assert data["LUT"] == "13:39:06"
        assert set(data) == {"type", "exchange_segment", "security_id", "LTP", "volume", "LTT", "LUT"}

    def test_prev_close(self, feed):
        data = feed.process_data(PREV_CLOSE)
        assert data["type"] == "Previous Close"
        assert data["prev_close"] == pytest.approx(0.9476, abs=1e-4)
        assert "prev_OI" not in data

    def test_circuit_limit(self, feed):
        data = feed.process_data(CIRCUIT_LIMIT)
        assert data["type"] == "Circuit Limit"
        assert data["upper_circuit"] == pytest.approx(1.2319, abs=1e-4)
        assert data["lower_circuit"] == pytest.approx(0.6633, abs=1e-4)

    def test_52_week(self, feed):
        data = feed.process_data(WEEK_52)
        assert data["type"] == "52 Week High Low"
        assert data["week_high"] == pytest.approx(2.09, abs=1e-4)
        assert data["week_low"] == pytest.approx(0.8823, abs=1e-4)

    def test_ohlc(self, feed):
        data = feed.process_data(OHLC)
        assert data == {"type": "OHLC", "exchange_segment": 14, "security_id": 10006001,
                        "open": "0.96", "close": "0.95", "high": "0.95", "low": "0.93"}

    def test_market_status(self, feed):
        packet = header(18, 29) + b'USA' + struct.pack('<i', 1)
        data = feed.process_data(packet)
        assert data["type"] == "Market Status"
        assert data["market_type"] == "USA"
        assert data["market_status"] == 1

    def test_concatenated_packets(self, feed):
        data = feed.process_data(TRADE + PREV_CLOSE + CIRCUIT_LIMIT + WEEK_52)
        assert [p["type"] for p in data] == ["Trade", "Previous Close", "Circuit Limit", "52 Week High Low"]

    def test_error_packet(self, feed):
        feed.on_close = MagicMock()
        data = feed.process_data(ERROR_807)
        assert data["type"] == "Error"
        assert data["error_code"] == 807
        assert data["message"] == "Token expired."
        feed.on_close.assert_called_once_with(feed)

    def test_zero_msg_length_falls_back_to_packet_size(self, feed):
        packet = bytearray(PREV_CLOSE)
        packet[9] = 0
        data = feed.process_data(bytes(packet) + TRADE)
        assert [p["type"] for p in data] == ["Previous Close", "Trade"]

    def test_truncated_packet_is_ignored(self, feed):
        data = feed.process_data(PREV_CLOSE + TRADE[:20])
        assert data["type"] == "Previous Close"

    def test_msg_length_shorter_than_packet_is_ignored(self, feed):
        packet = bytearray(TRADE)
        packet[9] = 15
        assert feed.process_data(bytes(packet)) == []

    def test_unknown_msg_code_is_skipped(self, feed):
        unknown = header(15, 99) + b'\x00' * 4
        data = feed.process_data(unknown + PREV_CLOSE)
        assert data["type"] == "Previous Close"
