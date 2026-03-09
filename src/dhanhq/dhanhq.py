"""
    A class that has core DhanHQ APIs.

    This library provides methods to manage orders, retrieve market data,
    and perform various trading operations through the DhanHQ API.

    :copyright: (c) 2025 by Dhan.
    :license: see LICENSE for details.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from webbrowser import open as web_open


from dhanhq import (Order, ForeverOrder, Portfolio, Statement, TraderControl, Security,
                    HistoricalData, OptionChain, MarketFeed, Funds, SuperOrder, ConditionalTrigger)


class dhanhq(Order, ForeverOrder, Portfolio, Funds, Statement, TraderControl, Security,
             MarketFeed, HistoricalData, OptionChain, SuperOrder, ConditionalTrigger):
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
                       MarketFeed, HistoricalData, OptionChain, SuperOrder, ConditionalTrigger]:
            parent.__init__(self,dhan_context)
        self.dhan_http = dhan_context.get_dhan_http()

    @staticmethod
    def convert_to_date_time(epoch):
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


def _save_as_temp_html_file_and_open_in_browser(form_html):
    """Module-level helper used by tests to mock opening edis form HTML."""
    temp_web_form_html = "temp_form.html"
    with open(temp_web_form_html, "w") as f:
        f.write(form_html)
    web_open(Path.cwd().joinpath(temp_web_form_html).as_uri())


# Provide a convenience wrapper on the composite class so tests patching
# `dhanhq.dhanhq._save_as_temp_html_file_and_open_in_browser` work and
# to avoid importing Security internals into tests.
def open_browser_for_tpin(self, isin, qty, exchange, segment='EQ', bulk=False):
    endpoint = '/edis/form'
    payload = {
        "isin": isin,
        "qty": qty,
        "exchange": exchange,
        "segment": segment,
        "bulk": bulk
    }
    response = self.dhan_http.post(endpoint, payload)
    from dhanhq.dhan_http import DhanHTTP
    if response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value:
        return response

    from json import loads as json_loads
    data = json_loads(response['data'])
    form_html = data.get('edisFormHtml', '')
    form_html = form_html.replace('\\', '')
    _save_as_temp_html_file_and_open_in_browser(form_html)
    return response


# Attach the wrapper to the dhanhq class so instance calls resolve to this
dhanhq.open_browser_for_tpin = open_browser_for_tpin
