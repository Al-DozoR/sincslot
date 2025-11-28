import re
from typing import Annotated, Union, Optional

import phonenumbers
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from pydantic import BaseModel, EmailStr, Field, field_validator

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
    repeat_password: str = Field(alias="repeatPassword")

    @field_validator('password')
    def validate_password_complexity(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву (A–Z)')
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву (a–z)')
        if not re.search(r'\d', v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру (0–9)')
        if not re.search(r'[!@#$%^&*()_+\-=]', v):
            raise ValueError('Пароль должен содержать хотя бы один спецсимвол: !@#$%^&*()_+-=')
        return v


class CompanyLoginRequest(BaseModel):
    email: EmailStr
    password: str


class CompanyRecoverPasswordRequest(BaseModel):
    email: str
