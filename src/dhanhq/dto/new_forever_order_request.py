from typing import Optional

# from pydantic.dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, field_validator, constr, Field

from dhanhq.constant import OrderType, Validity, OrderFlag
from dhanhq.constant import TransactionType, ExchangeSegment, ProductType
from dhanhq.helper import CommonUtils


# Use @dataclass if you want a lightweight solution and are okay with handling aliasing and serialization manually.
# Use BaseModel if you want built-in validation, aliasing, and serialization.
# @dataclass
class NewForeverOrderRequest(BaseModel):
    # Automatically generate camelCase aliases for all fields
    model_config = ConfigDict(alias_generator=CommonUtils.to_camel_case, populate_by_name=True)

    security_id: constr(strict=True)  # type: ignore  # Suppress Pyright error for Constrained string
    exchange_segment: ExchangeSegment # Pydantic will raise ValidationError if this value is not assigned
    transaction_type: TransactionType #
    product_type: ProductType #
    order_type: OrderType #
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)
    trigger_price: float = 0 # c-reqd StopLoss-Market and StopLoss-Limit orders
    order_flag: OrderFlag = OrderFlag.SINGLE  # Specific to ForeverOrder
    validity: Validity = Validity.DAY
    disclosed_quantity: int = 0 #
    price1: float = 0  # Specific to ForeverOrder
    trigger_price1: float = 0 # Specific to ForeverOrder
    quantity1: int = 0 # Specific to ForeverOrder
    correlation_id: Optional[str] = None # Specific to ForeverOrder

    @field_validator('security_id')
    def validate_security_id(cls, value): # custom_validation for mandatory field
        """
        Parameters
        ----------
        value

        Returns
        -------
        value: if the value is positive integer, otherwise raises ValueError
        """
        if not value.isdigit():
            raise ValueError("Security ID must be a positive integer.")
        if int(value) <= 0:
            raise ValueError("Security ID must be a positive integer.")
        return value
