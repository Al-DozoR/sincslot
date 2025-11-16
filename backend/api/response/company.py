from typing import Optional
from pydantic import BaseModel


class CreateCompanyResponse(BaseModel):
    id: int


class CompanyByIdResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    description: Optional[str]
    address: Optional[str]


class CompanyNotFoundByIdResponse(BaseModel):
    message: str