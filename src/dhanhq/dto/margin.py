from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, constr, Field

from dhanhq.helper import CommonUtils


class Margin(BaseModel):
    # Automatically generate camelCase aliases for all fields
    model_config = ConfigDict(alias_generator=CommonUtils.to_camel_case, populate_by_name=True)

    leverage: Optional[str] = Field(alias="leverage", default=None)
    totalMargin: Optional[float] = Field(alias="totalMargin", default=None)
    spanMargin: Optional[float] = Field(alias="spanMargin", default=None)
    exposureMargin: Optional[float] = Field(alias="exposureMargin", default=None)
    availableBalance: Optional[float] = Field(alias="availableBalance", default=None)
    variableMargin: Optional[float] = Field(alias="variableMargin", default=None)
    insufficientBalance: Optional[float] = Field(alias="insufficientBalance", default=None)