from pydantic import BaseModel, ConfigDict, field_validator, constr, Field

from dhanhq.constant import OrderType, Validity, LegName, OrderFlag, ExchangeSegment, TransactionType, ProductType
from dhanhq.helper import CommonUtils


class ComputeMarginRequest(BaseModel):
    security_id: constr(strict=True)  # type: ignore  # Suppress Pyright error for Constrained string
    exchange_segment: ExchangeSegment
    transaction_type: TransactionType
    quantity: int
    product_type: ProductType
    price: float
    trigger_price: float = 0

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
