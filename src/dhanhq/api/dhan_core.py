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


class DhanCore:
    """DhanHQ Class having Core APIs"""

    def __init__(self, dhan_context :DhanConnection):
        self.dhan_http = dhan_context.get_dhan_http()
        self.orderEndpoint = OrderEndpoint(dhan_context)
        self.foreverOrderEndpoint = ForeverOrderEndpoint(dhan_context)
        self.portfolioEndpoint = PortfolioEndpoint(dhan_context)
        self.fundsEndpoint = FundsEndpoint(dhan_context)
        self.statementEndpoint = StatementEndpoint(dhan_context)
        self.traderControlEndpoint = TraderControlEndpoint(dhan_context)
        self.securityEndpoint = SecurityEndpoint(dhan_context)
        self.marketFeedEndpoint = MarketFeedEndpoint(dhan_context)
        self.historicalDataEndpoint = HistoricalDataEndpoint(dhan_context)
        self.optionChainEndpoint = OptionChainEndpoint(dhan_context)

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
