from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class ServiceEntityResponse(BaseModel):
    id: int
    name: str
    duration: int
    price: int
    description: Optional[str] = Field(default=None)

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ServiceEntityListResponse(BaseModel):
    services: list[ServiceEntityResponse]


class ServiceErrorResponse(BaseModel):
    error: str
