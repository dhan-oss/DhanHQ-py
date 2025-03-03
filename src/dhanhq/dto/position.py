from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, Field

from dhanhq.constant import PositionType, ExchangeSegment, ProductType, OptionType
from dhanhq.helper import CommonUtils


class Position(BaseModel):
    # Automatically generate camelCase aliases for all fields
    model_config = ConfigDict(alias_generator=CommonUtils.to_camel_case, populate_by_name=True)

    security_id: Optional[str] = Field(alias="securityId", default=None)
    trading_symbol: Optional[str] = Field(alias="tradingSymbol", default=None)
    position_type: Optional[PositionType] = Field(alias="positionType", default=None)
    product_type: Optional[ProductType] = Field(alias="productType", default=None)
    exchange_segment: Optional[ExchangeSegment] = Field(alias="exchangeSegment", default=None)
    buy_qty: Optional[int] = Field(alias="buyQty", default=None)
    sell_qty: Optional[int] = Field(alias="sellQty", default=None)
    net_qty: Optional[int] = Field(alias="netQty", default=None)
    multiplier: Optional[int] = Field(alias="multiplier", default=None)
    carry_forward_buy_qty: Optional[int] = Field(alias="carryForwardBuyQty", default=None)
    carry_forward_sell_qty: Optional[int] = Field(alias="carryForwardSellQty", default=None)
    carry_forward_buy_value: Optional[int] = Field(alias="carryForwardBuyValue", default=None)
    carry_forward_sell_value: Optional[int] = Field(alias="carryForwardSellValue", default=None)
    day_buy_qty: Optional[int] = Field(alias="daySellQty", default=None)
    day_sell_qty: Optional[int] = Field(alias="daySellQty", default=None)
    drv_expiry_date: Optional[str] = Field(alias="drvExpiryDate", default=None)
    drv_option_type: Optional[OptionType] = Field(alias="drvOptionType", default=None)
    cross_currency: Optional[bool] = Field(alias="crossCurrency", default=None)
    buy_avg: Optional[float] = Field(alias="buyAvg", default=None)
    sell_avg: Optional[float] = Field(alias="sellAvg", default=None)
    cost_price: Optional[float] = Field(alias="costPrice", default=None)
    realized_profit: Optional[float] = Field(alias="realizedProfit", default=None)
    unrealized_profit: Optional[float] = Field(alias="unrealizedProfit", default=None)
    rbi_reference_rate: Optional[float] = Field(alias="rbiReferenceRate", default=None)
    day_buy_value: Optional[float] = Field(alias="dayBuyValue", default=None)
    day_sell_value: Optional[float] = Field(alias="daySellValue", default=None)
    drv_strike_price: Optional[float] = Field(alias="drvStrikePrice", default=None)

    @field_validator('position_type', 'product_type', 'exchange_segment', 'drv_option_type',
                     mode='before')
    def convert_string_to_enum(cls, value, field):
        try:
            if isinstance(value, str):
                if not value: # Check for empty string
                    return None
                # Determine which enum to use based on the field name
                if field.field_name == "position_type":
                    return PositionType[value]
                elif field.field_name == "product_type":
                    return ProductType[value]
                elif field.field_name == "exchange_segment":
                    return ExchangeSegment[value]
                elif field.field_name == "drv_option_type":
                    return OptionType[value]
            return value
        except KeyError:
            return None