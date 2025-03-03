from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, constr

from dhanhq.constant import LegName, OptionType, OrderFlag
from dhanhq.constant import TransactionType, ExchangeSegment, ProductType, OrderStatus
from dhanhq.helper import CommonUtils


class ForeverOrder(BaseModel):
    # Automatically generate camelCase aliases for all fields
    model_config = ConfigDict(alias_generator=CommonUtils.to_camel_case, populate_by_name=True)

    order_flag: OrderFlag

    order_id: str
    order_status: OrderStatus
    transaction_type: TransactionType
    exchange_segment: ExchangeSegment
    product_type: ProductType
    trading_symbol: str
    security_id: str
    quantity: int
    price: float
    trigger_price: float
    leg_name:LegName
    create_time: str
    update_time: str
    exchange_time: str
    drv_expiry_date: constr(strict=True)  # type: ignore  # Suppress Pyright error for Constrained string
    drv_option_type: Optional[OptionType]
    drv_strike_price: float

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
                     'product_type', 'order_flag',
                     'leg_name', 'drv_option_type',
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
                elif field.field_name == "order_flag":
                    return OrderFlag[value]
                elif field.field_name == "leg_name":
                    return LegName[value]
                elif field.field_name == "drv_option_type":
                    return OptionType[value]
            return value
        except KeyError:
            return None