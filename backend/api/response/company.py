from typing import Optional
from pydantic import BaseModel


class CompanyTokensResponse(BaseModel):
    access_token: str
    refresh_token: str


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
    message: str


class CompanyRecoverPasswordResponse(BaseModel):
    login: str
    new_password: str
