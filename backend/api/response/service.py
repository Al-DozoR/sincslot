from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class ServiceEntityResponse(BaseModel):
    id: int
    duration: int
    price: int
    company_id: Optional[int] = Field(default=None, alias="companyID")
    client_id: Optional[int] = Field(default=None, alias="companyID")
    updated_at: Optional[int] = Field(default=None, alias="updatedAt")
    created_at: Optional[int] = Field(default=None, alias="createdAt")
    description: Optional[str] = Field(default=None)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

class ServiceErrorResponse(BaseModel):
    error: str
