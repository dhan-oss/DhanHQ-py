from pydantic import BaseModel, ConfigDict, field_validator, constr, Field

from dhanhq.constant import OrderType, Validity, LegName
from dhanhq.helper import CommonUtils


class ModifyOrderRequest(BaseModel):
    # Automatically generate camelCase aliases for all fields
    model_config = ConfigDict(alias_generator=CommonUtils.to_camel_case, populate_by_name=True)

    order_id: constr(strict=True)  # type: ignore  # Suppress Pyright error for Constrained string
    order_type: OrderType #
    leg_name: LegName #
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    disclosed_quantity: int = 0 #
    trigger_price: float = 0 # c-reqd StopLoss-Market and StopLoss-Limit orders
    validity: Validity = Validity.DAY

    @field_validator('order_id')
    def validate_order_id(cls, value): # custom_validation for mandatory field
        """

        Parameters
        ----------
        value

        Returns
        -------
        value: if the value is positive integer, otherwise raises ValueError
        """
        if not value.isdigit():
            raise ValueError("Order ID must be a positive integer.")
        if int(value) <= 0:
            raise ValueError("Order ID must be a positive integer.")
        return value
