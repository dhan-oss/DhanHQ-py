from unittest.mock import patch


class TestDhanhq_MarketAnalytics:
    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_technical_data(self, mock_post, dhanhq_obj):
        dhanhq_obj.technical_data("14366", "NSE_EQ", "EQUITY", "D", ["SMA_20", "RSI_14"])
        mock_post.assert_called_once_with('/data/technical', {
            "securityId": "14366",
            "exchangeSegment": "NSE_EQ",
            "instrument": "EQUITY",
            "timeframe": "D",
            "indicators": ["SMA_20", "RSI_14"]
        })

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_technical_data_casts_ids_and_accepts_single_indicator(self, mock_post, dhanhq_obj):
        dhanhq_obj.technical_data(13, "IDX_I", "INDEX", 5, "EMA_20")
        payload = mock_post.call_args[0][1]
        assert payload["securityId"] == "13"
        assert payload["timeframe"] == "5"
        assert payload["indicators"] == ["EMA_20"]

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_company_info(self, mock_post, dhanhq_obj):
        dhanhq_obj.company_info("14366", "NSE_EQ", ["CO", "RATIOS", "SHP"])
        mock_post.assert_called_once_with('/data/companyinfo', {
            "securityId": "14366",
            "exchangeSegment": "NSE_EQ",
            "instrument": "EQUITY",
            "metrics": ["CO", "RATIOS", "SHP"]
        })

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_market_movers_equity(self, mock_post, dhanhq_obj):
        dhanhq_obj.market_movers("NSE_EQ", ["EQUITY"], "PRICE_GAINERS", universe="NIFTY_50", limit=5)
        mock_post.assert_called_once_with('/data/marketmovers', {
            "exchangeSegment": "NSE_EQ",
            "instrument": ["EQUITY"],
            "category": "PRICE_GAINERS",
            "universe": "NIFTY_50",
            "limit": 5
        })

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_market_movers_omits_unset_optional_fields(self, mock_post, dhanhq_obj):
        dhanhq_obj.market_movers("NSE_FNO", "OPTIDX", "HIGHEST_OI", expiry="2026-11-25")
        mock_post.assert_called_once_with('/data/marketmovers', {
            "exchangeSegment": "NSE_FNO",
            "instrument": ["OPTIDX"],
            "category": "HIGHEST_OI",
            "expiry": "2026-11-25"
        })

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_news_headline_defaults(self, mock_post, dhanhq_obj):
        dhanhq_obj.news_headline()
        mock_post.assert_called_once_with('/data/newsheadline', {"categories": ["ALL"], "limit": 10})

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_news_headline_with_filters(self, mock_post, dhanhq_obj):
        dhanhq_obj.news_headline(["COMPANIES", "IPO"], 20, universe="WATCHLIST", stock_list=[14366, "1333"])
        mock_post.assert_called_once_with('/data/newsheadline', {
            "categories": ["COMPANIES", "IPO"],
            "limit": 20,
            "universe": "WATCHLIST",
            "stockList": ["14366", "1333"]
        })

    @patch("requests.Session.post")
    def test_news_headline_sends_client_id(self, mock_session_post, dhanhq_obj):
        mock_session_post.return_value.status_code = 200
        mock_session_post.return_value.content = b'{"data": {"latestNews": []}}'
        response = dhanhq_obj.news_headline(limit=1)
        assert '"dhanClientId": "test_client_id"' in mock_session_post.call_args.kwargs["data"]
        assert response["status"] == "success"
        assert response["data"] == {"data": {"latestNews": []}}
