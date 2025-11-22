from pydantic import BaseModel
from typing import Optional


class CompanyCreateRequest(BaseModel):
    name: str
    address: Optional[str] = None
    email: str
    phone: Optional[str] = None
    password: str
    repeat_password: str


class CompanyLoginRequest(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    password: str


class CompanyRefreshTokenRequest(BaseModel):
    refresh_token: str


class CompanyRecoverPasswordRequest(BaseModel):
    email: str
