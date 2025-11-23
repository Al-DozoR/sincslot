from typing import Annotated, Union, Optional

import phonenumbers
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from pydantic import BaseModel, EmailStr

E164NumberType = Annotated[
    Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(number_format="E164")
]


class CompanyPhoneNumberRequest(BaseModel):
    phone: E164NumberType


class CompanyCreateRequest(BaseModel):
    name: str
    address: Optional[str] = None
    email: EmailStr
    phone: E164NumberType = None
    password: str
    repeat_password: str


class CompanyLoginRequest(BaseModel):
    email: EmailStr
    password: str


class CompanyRefreshTokenRequest(BaseModel):
    refresh_token: str


class CompanyRecoverPasswordRequest(BaseModel):
    email: str
