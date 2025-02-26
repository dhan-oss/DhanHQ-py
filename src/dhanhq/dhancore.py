"""
    A class that has core DhanHQ APIs.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2024 by Dhan.
    :license: see LICENSE for details.
"""

from datetime import datetime, timedelta, timezone, date
from typing import Union

from dhanhq import (Order, ForeverOrder, Portfolio, Statement, TraderControl, Security,
                    HistoricalData, OptionChain, MarketFeed, Funds, DhanContext)


class DhanCore(Order, ForeverOrder, Portfolio, Funds, Statement, TraderControl, Security,
               MarketFeed, HistoricalData, OptionChain):
    """DhanHQ Class having Core APIs"""

    def __init__(self, dhan_context :DhanContext):
        for parent in [Order, ForeverOrder, Portfolio, Funds, Statement, TraderControl, Security,
                       MarketFeed, HistoricalData, OptionChain]:
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
