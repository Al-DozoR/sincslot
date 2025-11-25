from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class CompanyTokensResponse(BaseModel):
    access_token: str = Field(alias="accessToken")
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyByIdResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    description: Optional[str]
    address: Optional[str]


class CompaniesList(BaseModel):
    companies: list[CompanyByIdResponse]


class CompanyErrorResponse(BaseModel):
    error: str
