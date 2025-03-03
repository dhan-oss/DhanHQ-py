from unittest.mock import patch

from dhanhq.constant import ExchangeSegment, PositionType, ProductType
from dhanhq.dto import ConvertPositionRequest


class TestPortfolioEndpoint:
    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_positions(self, mock_read_request, dhanhq_obj):
        mock_read_request.return_value = [
            {
                "dhanClientId": "1000000009",
                "tradingSymbol": "TCS",
                "securityId": "11536",
                "positionType": "LONG",
                "exchangeSegment": "NSE_EQ",
                "productType": "CNC",
                "buyAvg": 3345.8,
                "buyQty": 40,
                "costPrice": 3215.0,
                "sellAvg": 0.0,
                "sellQty": 0,
                "netQty": 40,
                "realizedProfit": 0.0,
                "unrealizedProfit": 6122.0,
                "rbiReferenceRate": 1.0,
                "multiplier": 1,
                "carryForwardBuyQty": 0,
                "carryForwardSellQty": 0,
                "carryForwardBuyValue": 0.0,
                "carryForwardSellValue": 0.0,
                "dayBuyQty": 40,
                "daySellQty": 0,
                "dayBuyValue": 133832.0,
                "daySellValue": 0.0,
                "drvExpiryDate": "0001-01-01",
                "drvOptionType": "",
                "drvStrikePrice": 0.0,
                "crossCurrency": False
            }
        ]
        dhanhq_obj.portfolioEndpoint.get_current_positions()
        mock_read_request.assert_called_once_with('/positions')

    @patch("dhanhq.http.DhanHTTP.get")
    def test_get_holdings(self, mock_read_request, dhanhq_obj):
        mock_read_request.return_value = [
            {
                "exchange": "ALL",
                "tradingSymbol": "HDFC",
                "securityId": "1330",
                "isin": "INE001A01036",
                "totalQty": 1000,
                "dpQty": 1000,
                "t1Qty": 0,
                "availableQty": 1000,
                "collateralQty": 0,
                "avgCostPrice": 2655.0,
                # "lastTradedPrice": 0
            }
        ]
        dhanhq_obj.portfolioEndpoint.get_current_holdings()
        mock_read_request.assert_called_once_with('/holdings')

    @patch("dhanhq.http.DhanHTTP.post")
    def test_convert_position(self, mock_create_request, dhanhq_obj):
        convertPositionRequest = ConvertPositionRequest(security_id="1",
                                               position_type=PositionType.LONG,
                                               exchange_segment=ExchangeSegment.NSE_EQ,
                                               convert_qty=10,
                                               from_product_type=ProductType.CNC,
                                               to_product_type=ProductType.INTRADAY)
        dhanhq_obj.portfolioEndpoint.convert_position(convertPositionRequest)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == '/positions/convert'
