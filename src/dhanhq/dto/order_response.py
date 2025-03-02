from pydantic import Field, validator, field_validator, BaseModel

from pydantic.dataclasses import dataclass

from dhanhq.constant import OrderStatus


class OrderResponse(BaseModel):
    order_id: str = Field(alias="orderId")
    order_status: OrderStatus = Field(alias="orderStatus")

    @field_validator('order_status', mode='before')
    def convert_string_to_enum(cls, value):
        # Determine the field being validated
        if isinstance(value, str):
            # Convert string to enum name
                return OrderStatus[value]
        return value