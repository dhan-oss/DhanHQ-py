"""
    A class that has core DhanHQ APIs.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2024 by Dhan.
    :license: see LICENSE for details.
"""

from datetime import datetime, timedelta, timezone, date
from typing import Union

from dhanhq.api import DhanConnection
from dhanhq.api.ondemand import (OrderEndpoint, ForeverOrderEndpoint, PortfolioEndpoint, StatementEndpoint,
                                 TraderControlEndpoint, SecurityEndpoint, HistoricalDataEndpoint, OptionChainEndpoint,
                                 MarketFeedEndpoint, FundsEndpoint)


class DhanCore(OrderEndpoint, ForeverOrderEndpoint, PortfolioEndpoint, FundsEndpoint,
               StatementEndpoint, TraderControlEndpoint, SecurityEndpoint,
               MarketFeedEndpoint, HistoricalDataEndpoint, OptionChainEndpoint):
    """DhanHQ Class having Core APIs"""

    def __init__(self, dhan_context :DhanConnection):
        for parent in [OrderEndpoint, ForeverOrderEndpoint, PortfolioEndpoint, FundsEndpoint, StatementEndpoint,
                       TraderControlEndpoint, SecurityEndpoint, MarketFeedEndpoint, HistoricalDataEndpoint,
                       OptionChainEndpoint]:
            parent.__init__(self,dhan_context)
        self.dhan_http = dhan_context.get_dhan_http()

    @staticmethod
    def convert_to_date_time(epoch :int) -> Union[datetime, date]:
        """
        Convert EPOCH time to Python datetime object in IST.

        Args:
            epoch (int): The EPOCH time to convert.

        Returns:
            Union[datetime, date]: Corresponding datetime or date object in IST.
        """
        IST = timezone(timedelta(hours=5, minutes=30))
        dt = datetime.fromtimestamp(epoch, IST)

        if dt.time() == datetime.min.time():
            return dt.date()
        return dt
