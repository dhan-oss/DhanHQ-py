"""
    A class that has core DhanHQ APIs.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2025 by Dhan.
    :license: see LICENSE for details.
"""

from datetime import datetime, timedelta, timezone


from dhanhq import (Order, ForeverOrder, Portfolio, Statement, TraderControl, Security,
                    HistoricalData, OptionChain, MarketFeed, Funds)


class dhanhq(Order, ForeverOrder, Portfolio, Funds, Statement, TraderControl, Security,
             MarketFeed, HistoricalData, OptionChain):
    """DhanHQ Class having Core APIs"""

    """Constants for Exchange Segment"""
    NSE = 'NSE_EQ'
    BSE = 'BSE_EQ'
    CUR = 'NSE_CURRENCY'
    MCX = 'MCX_COMM'
    FNO = 'NSE_FNO'
    NSE_FNO = 'NSE_FNO'
    BSE_FNO = 'BSE_FNO'
    INDEX = 'IDX_I'

    """Constants for Transaction Type"""
    BUY = 'BUY'
    SELL = 'SELL'

    """Constants for Product Type"""
    CNC = 'CNC'
    INTRA = "INTRADAY"
    MARGIN = 'MARGIN'
    CO = 'CO'
    BO = 'BO'
    MTF = 'MTF'

    """Constants for Order Type"""
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    SL = "STOP_LOSS"
    SLM = "STOP_LOSS_MARKET"

    """Constants for Validity"""
    DAY = 'DAY'
    IOC = 'IOC'


    def __init__(self, dhan_context):
        for parent in [Order, ForeverOrder, Portfolio, Funds, Statement, TraderControl, Security,
                       MarketFeed, HistoricalData, OptionChain]:
            parent.__init__(self,dhan_context)
        self.dhan_http = dhan_context.get_dhan_http()

    @staticmethod
    def convert_to_date_time(self, epoch):
        """
        Convert EPOCH time to Python datetime object in IST.

        Args:
            epoch (int): The EPOCH time to convert.

        Returns:
            datetime: Corresponding datetime object in IST.
        """
        IST = timezone(timedelta(hours=5, minutes=30))
        dt = datetime.fromtimestamp(epoch, IST)

        if dt.time() == datetime.min.time():
            return dt.date()
        return dt
