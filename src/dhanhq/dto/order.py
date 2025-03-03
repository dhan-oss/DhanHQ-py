from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, constr, Field

from dhanhq.constant import OrderType, Validity, LegName, OptionType
from dhanhq.constant import TransactionType, ExchangeSegment, ProductType, OrderStatus
from dhanhq.helper import CommonUtils


class Order(BaseModel):
    # Automatically generate camelCase aliases for all fields
    model_config = ConfigDict(alias_generator=CommonUtils.to_camel_case, populate_by_name=True)

    order_id: Optional[str] = Field(alias="orderId", default=None)
    correlation_id: Optional[str] = Field(alias="correlationId", default=None)
    order_status: Optional[OrderStatus] = Field(alias="orderStatus", default=None)
    transaction_type: Optional[TransactionType] = Field(alias="transactionType", default=None)
    exchange_segment: Optional[ExchangeSegment] = Field(alias="exchangeSegment", default=None)
    product_type: Optional[ProductType] = Field(alias="productType", default=None)
    order_type: Optional[OrderType] = Field(alias="orderType", default=None)
    validity: Optional[Validity] = Field(alias="validity", default=None)
    trading_symbol: Optional[str] = Field(alias="tradingSymbol", default=None)
    security_id: Optional[str] = Field(alias="securityId", default=None)
    quantity: Optional[int] = Field(alias="quantity", default=None)
    disclosed_quantity: Optional[int] = Field(alias="disclosedQuantity", default=None)
    price: Optional[float] = Field(alias="price", default=None)
    trigger_price: Optional[float] = Field(alias="triggerPrice", default=None)
    after_market_order: Optional[bool] = Field(alias="afterMarketOrder", default=None)
    bo_profit_value: Optional[float] = Field(alias="boProfitValue", default=None)
    bo_stop_loss_Value: Optional[float] = Field(alias="boStopLossValue", default=None)
    leg_name:Optional[LegName] = Field(alias="legName", default=None)
    create_time: Optional[str] = Field(alias="createTime", default=None)
    update_time: Optional[str] = Field(alias="updateTime", default=None)
    exchange_time: Optional[str] = Field(alias="exchangeTime", default=None)
    drv_expiry_date: constr(strict=True)  # type: ignore  # Suppress Pyright error for Constrained string
    drv_option_type: Optional[OptionType] = Field(alias="drvOptionType", default=None)
    drv_strike_price: Optional[float] = Field(alias="drvStrikePrice", default=None)
    oms_error_code: Optional[str] = Field(alias="omsErrorCode", default=None)
    oms_error_description: Optional[str] = Field(alias="omsErrorDescription", default=None)
    algo_id: Optional[str] = Field(alias="algoId", default=None)
    remaining_quantity: Optional[int] = Field(alias="remainingQuantity", default=None)
    average_traded_price: Optional[int] = Field(alias="averageTradedPrice", default=None)
    filled_qty: Optional[int] = Field(alias="filledQty", default=None)

    @field_validator('drv_expiry_date')
    def validate_drv_expiry_date(cls, value): # custom_validation for mandatory field
        """

        Parameters
        ----------
        value

        Returns
        -------
        value: if the value is positive integer, otherwise raises ValueError
        """
        if not value.isdigit():
            return ""
        return value

    @field_validator('order_status', 'transaction_type', 'exchange_segment',
                     'product_type', 'order_type', 'validity', 'leg_name', 'drv_option_type',
                     mode='before')
    def convert_string_to_enum(cls, value, field):
        try:
            if isinstance(value, str):
                # Determine which enum to use based on the field name
                if field.field_name == "order_status":
                    return OrderStatus[value]
                elif field.field_name == "transaction_type":
                    return TransactionType[value]
                elif field.field_name == "exchange_segment":
                    return ExchangeSegment[value]
                elif field.field_name == "product_type":
                    return ProductType[value]
                elif field.field_name == "order_type":
                    return OrderType[value]
                elif field.field_name == "validity":
                    return Validity[value]
                elif field.field_name == "leg_name":
                    return LegName[value]
                elif field.field_name == "drv_option_type":
                    return OptionType[value]
            return value
        except KeyError:
            return None