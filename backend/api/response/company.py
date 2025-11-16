from typing import Optional
from pydantic import BaseModel


class CreateCompanyResponse(BaseModel):
    access_token: str
    refresh_token: str


class CreateCompanyErrorResponse(BaseModel):
    message: str


class CompanyByIdResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    description: Optional[str]
    address: Optional[str]


class CompanyNotFoundByIdResponse(BaseModel):
    message: str