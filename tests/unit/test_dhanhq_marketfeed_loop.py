import asyncio
import struct
from unittest.mock import AsyncMock, MagicMock

import pytest

from dhanhq import MarketFeed, DhanContext


def _ticker_packet():
    return struct.pack("<BHBIfI", 2, 0, 1, 1333, 100.5, 1700000000)


@pytest.fixture
def feed():
    context = DhanContext("client_id", "access_token")
    feed = MarketFeed(context, [(1, "1333", 15)])
    yield feed
    if not feed.loop.is_closed():
        feed.loop.close()


async def _ping():
    await asyncio.sleep(0)
    return "pong"


class TestMarketFeedEventLoop:
    def test_run_sync_without_running_loop(self, feed):
        assert feed._run_sync(_ping()) == "pong"

    def test_run_sync_inside_running_loop(self, feed):
        async def main():
            task = feed._run_sync(_ping())
            assert isinstance(task, asyncio.Task)
            return await task

        assert asyncio.run(main()) == "pong"

    def test_get_data_inside_running_loop(self, feed):
        feed.ws = MagicMock()
        feed.ws.recv = AsyncMock(return_value=_ticker_packet())

        async def main():
            task = feed.get_data()
            assert isinstance(task, asyncio.Task)
            return await task

        data = asyncio.run(main())
        assert data["LTP"] == "{:.2f}".format(100.5)
        assert data["security_id"] == 1333

    def test_run_forever_inside_running_loop(self, feed):
        feed.connect = AsyncMock()

        async def main():
            task = feed.run_forever()
            assert isinstance(task, asyncio.Task)
            await task
            return True

        assert asyncio.run(main()) is True
        feed.connect.assert_awaited_once()
