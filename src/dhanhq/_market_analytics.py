class MarketAnalytics:
    """
    Market Analytics Data APIs: Technical Data, Company Info, Market Movers and Live News Headline.

    These APIs need an active Data API subscription. Technical Data, Market Movers and
    Live News Headline need the Pro Traders Plan.
    """

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    @staticmethod
    def _as_list(value):
        """Allow a single string where the API expects an array."""
        if isinstance(value, str):
            return [value]
        return list(value)

    def technical_data(self, security_id, exchange_segment, instrument, timeframe, indicators):
        """
        Retrieve technical indicator values for a stock or an index, as of the latest
        closed candle for the requested timeframe.

        Args:
            security_id (str): Exchange standard ID of the security, e.g. '14366'.
            exchange_segment (str): 'NSE_EQ' or 'IDX_I'.
            instrument (str): 'EQUITY' or 'INDEX'.
            timeframe (str): Candle size used for all indicators: '1', '5', '15' or 'D'.
            indicators (list): Indicator identifiers, e.g. ['SMA_20', 'RSI_14', 'MACD_HIST'].
                Supported: SMA_5/10/20/50/100/200, EMA_5/10/20/50/100/200, RSI_14, MACD_HIST,
                STOCH, STOCHRSI_14, ATR_14, ADX_14, UO, ROC, WILLR, PIVOT_CLASSIC,
                PIVOT_FIBONACCI, PIVOT_CAMARILLA.

        Returns:
            dict: The response containing indicator values. Moving averages are grouped by
                type (e.g. data['SMA'] is a list of {'period', 'value', 'action'}), pivots are
                grouped under data['PIVOT'], and other indicators are keyed by name.
        """
        endpoint = '/data/technical'
        payload = {
            "securityId": str(security_id),
            "exchangeSegment": exchange_segment,
            "instrument": instrument,
            "timeframe": str(timeframe),
            "indicators": self._as_list(indicators)
        }
        return self.dhan_http.post(endpoint, payload)

    def company_info(self, security_id, exchange_segment, metrics, instrument='EQUITY'):
        """
        Retrieve fundamental metrics for a single equity instrument.

        Args:
            security_id (str): Exchange standard ID of the security, e.g. '14366'.
            exchange_segment (str): 'NSE_EQ' or 'BSE_EQ'.
            metrics (list): Metric sections to fetch: 'CO' (Company Overview),
                'RATIOS' (Return Ratios) and/or 'SHP' (Shareholding Pattern).
            instrument (str): Instrument type. Only 'EQUITY' is supported (default).

        Returns:
            dict: The response containing the requested metric sections, keyed by section.
        """
        endpoint = '/data/companyinfo'
        payload = {
            "securityId": str(security_id),
            "exchangeSegment": exchange_segment,
            "instrument": instrument,
            "metrics": self._as_list(metrics)
        }
        return self.dhan_http.post(endpoint, payload)

    def market_movers(self, exchange_segment, instrument, category, expiry=None, universe=None, limit=None):
        """
        Retrieve top options, futures or stocks ranked by open interest, volume or price movement.

        Args:
            exchange_segment (str): 'NSE_EQ', 'BSE_EQ', 'NSE_FNO', 'BSE_FNO', 'NSE_COMM' or 'MCX_COMM'.
            instrument (list): Instrument types from a single group - options ('OPTIDX', 'OPTSTK',
                'OPTFUT'), futures ('FUTIDX', 'FUTSTK', 'FUTCOM') or stocks ('EQUITY').
            category (str): 'HIGHEST_OI' (options), 'OI_GAINERS', 'OI_LOSERS', 'TOP_VOLUME'
                (options, futures), 'PRICE_GAINERS' or 'PRICE_LOSERS' (stocks).
            expiry (str): Expiry date in YYYY-MM-DD. Required for options and futures.
            universe (str): Stock universe for EQUITY, e.g. 'ALL', 'NIFTY_50', 'FNO_STOCKS'.
            limit (int): Maximum number of instruments to return (1-100).

        Returns:
            dict: The response containing a ranked list of instruments under 'data'.
        """
        endpoint = '/data/marketmovers'
        payload = {
            "exchangeSegment": exchange_segment,
            "instrument": self._as_list(instrument),
            "category": category
        }
        if expiry is not None:
            payload["expiry"] = expiry
        if universe is not None:
            payload["universe"] = universe
        if limit is not None:
            payload["limit"] = limit
        return self.dhan_http.post(endpoint, payload)

    def news_headline(self, categories=None, limit=10, universe=None, stock_list=None):
        """
        Retrieve the latest news headlines with sentiment, filterable by category and stock.

        Args:
            categories (list): News categories, e.g. ['ALL'] (default), ['COMPANIES', 'IPO'].
            limit (int): Number of news items to return, counted back from now (1-50). Default 10.
            universe (str): Scope news to 'PORTFOLIO' or 'WATCHLIST'. Omitted by default.
            stock_list (list): Security IDs to filter news by specific stocks.

        Returns:
            dict: The response containing the headlines under data['latestNews'].
        """
        endpoint = '/data/newsheadline'
        payload = {
            "categories": self._as_list(categories) if categories is not None else ["ALL"],
            "limit": limit
        }
        if universe is not None:
            payload["universe"] = universe
        if stock_list is not None:
            payload["stockList"] = [str(s) for s in self._as_list(stock_list)]
        return self.dhan_http.post(endpoint, payload)
