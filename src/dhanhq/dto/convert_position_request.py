from pydantic import BaseModel, field_validator, constr

from dhanhq.constant import ExchangeSegment, ProductType
from dhanhq.constant import PositionType


class ConvertPositionRequest(BaseModel):
    security_id: constr(strict=True)  # type: ignore  # Suppress Pyright error for Constrained string
    position_type: PositionType
    exchange_segment: ExchangeSegment
    convert_qty: int
    from_product_type: ProductType
    to_product_type: ProductType

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
