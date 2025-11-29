import re
from datetime import datetime
from typing import Annotated, Union, Optional, Self

import phonenumbers
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, model_validator
from pydantic.alias_generators import to_camel

from backend.entity.company import DaysOfWeek

E164NumberType = Annotated[
    Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(number_format="E164")
]


class CompanyPhoneNumberRequest(BaseModel):
    phone: E164NumberType


class CompanyCreateRequest(BaseModel):
    name: str = Field(default="Apple")
    address: Optional[str] = None
    email: EmailStr = Field(default="SteveJobs123@example.com")
    phone: E164NumberType = Field(default="+79126329303")
    password: str = Field(default="Pass123!")
    repeat_password: str = Field(default="Pass123!", alias="repeatPassword")

    @classmethod
    @field_validator('password')
    def validate_password_complexity(cls, password):
        if not re.search(r'[A-Z]', password):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву (A–Z)')
        if not re.search(r'[a-z]', password):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву (a–z)')
        if not re.search(r'\d', password):
            raise ValueError('Пароль должен содержать хотя бы одну цифру (0–9)')
        if not re.search(r'[!@#$%^&*()_+\-=]', password):
            raise ValueError('Пароль должен содержать хотя бы один спецсимвол: !@#$%^&*()_+-=')
        return password


class CompanyLoginRequest(BaseModel):
    email: EmailStr
    password: str


class CompanyRecoverPasswordRequest(BaseModel):
    email: str


class CompanyWorkDay(BaseModel):
    day_of_week: DaysOfWeek = Field(default=DaysOfWeek.Monday)
    work_start: str = Field(default="9:00", alias="workStart")
    work_end: str = Field(default="18:00", alias="workEnd")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    @classmethod
    @field_validator("work_start", "work_end")
    def validate_time_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%H:%M")
        except:
            raise ValueError("Время должно быть в формате HH:MM (например, 9:00 или 18:30)")
        return value

    @model_validator(mode="after")
    def validate_work_hours(self) -> Self:
        start_hours, start_minutes = map(int, self.work_start.split(":"))
        end_hours, end_minutes = map(int, self.work_end.split(":"))

        if start_hours * 60 + start_minutes >= end_hours * 60 + end_minutes:
            raise ValueError("work_start должно быть раньше work_end")
        return self


class CompanyRequestWorkSchedule(BaseModel):
    work_schedule: list[CompanyWorkDay] = Field(alias="workSchedule")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
