from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, Field

from dhanhq.constant import Exchange
from dhanhq.helper import CommonUtils


class Holding(BaseModel):
    # Automatically generate camelCase aliases for all fields
    model_config = ConfigDict(alias_generator=CommonUtils.to_camel_case, populate_by_name=True)

    security_id: Optional[str] = Field(alias="securityId", default=None)
    trading_symbol: Optional[str] = Field(alias="tradingSymbol", default=None)
    isin: Optional[str] = Field(alias="isin", default=None)
    exchange: Optional[Exchange] = Field(alias="exchange", default=None)
    total_qty: Optional[int] = Field(alias="totalQty", default=None)
    dp_qty: Optional[int] = Field(alias="dpQty", default=None)
    t1_qty: Optional[int] = Field(alias="t1Qty", default=None)
    available_qty: Optional[int] = Field(alias="availableQty", default=None)
    collateral_qty: Optional[int] = Field(alias="collateralQty", default=None)
    avg_cost_price: Optional[float] = Field(alias="avgCostPrice", default=None)
    last_traded_price: Optional[float] = Field(alias="lastTradedPrice", default=None)

    @field_validator('exchange', mode='before')
    def convert_string_to_enum(cls, value):
        # Determine the field being validated
        if isinstance(value, str):
            # Convert string to enum name
                return Exchange[value]
        return value