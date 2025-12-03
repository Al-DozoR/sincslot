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


class CompanyCreateRequest(BaseModel):
    name: str = Field(examples=["Apple"])
    address: Optional[str] = None
    email: EmailStr = Field(examples=["SteveJobs123@example.com"])
    phone: E164NumberType = Field(examples=["+79126329303"])
    password: str = Field(examples=["Pass123!"])
    repeat_password: str = Field(examples=["Pass123!"], alias="repeatPassword")

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
    day_of_week: DaysOfWeek = Field(examples=[DaysOfWeek.Monday], alias="dayOfWeek")
    work_start: str = Field(examples=["9:00"], alias="workStart")
    work_end: str = Field(examples=["18:00"], alias="workEnd")

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


class CompanyWorkScheduleRequest(BaseModel):
    work_schedule: list[CompanyWorkDay] = Field(alias="workSchedule")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyUpdateSettingsRequest(BaseModel):
    name: Optional[str] = Field(default=None, examples=["Tesla"])
    address: Optional[str] = None
    email: Optional[EmailStr | None] = Field(default=None, examples=["ElonMask@example.ru"])
    phone: Optional[E164NumberType | None] = Field(default=None, examples=["+79125483496"])
    current_password: Optional[str] = Field(default=None, examples=["currentPass123"], alias="currentPassword")
    new_password: Optional[str] = Field(default=None, examples=["newPass123!"], alias="newPassword")
    new_repeat_password: Optional[str] = Field(
        default=None,
        examples=["user@example.ru"],
        alias="newRepeatPassword"
    )
    slug_booking_url: Optional[str] = Field(default=None, examples=["company name slug"], alias="slugBookingUrl")
    description: Optional[str] = Field(default=None, examples=["company description"])

    @classmethod
    @field_validator('new_password')
    def validate_password_complexity(cls, new_password):
        if not re.search(r'[A-Z]', new_password):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву (A–Z)')
        if not re.search(r'[a-z]', new_password):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву (a–z)')
        if not re.search(r'\d', new_password):
            raise ValueError('Пароль должен содержать хотя бы одну цифру (0–9)')
        if not re.search(r'[!@#$%^&*()_+\-=]', new_password):
            raise ValueError('Пароль должен содержать хотя бы один спецсимвол: !@#$%^&*()_+-=')

        return new_password

    @classmethod
    @field_validator('slug_booking_url')
    def validate_slug_booking_url(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        if not re.fullmatch(r"^[a-zA-Z-]+$", value):
            raise ValueError("slug_booking_url must contain only Latin letters and hyphens (-)")

        return value

    @model_validator(mode='after')
    def check_password_match(self) -> Self:
        if self.new_password is None and self.new_repeat_password is None:
            return self

        if self.new_password is None and self.new_repeat_password is not None:
            raise ValueError('new_password and new_repeat_password do not match')

        if self.new_password is not None and self.new_repeat_password is None:
            raise ValueError('new_password and new_repeat_password do not match')

        if self.new_password is not None and self.new_repeat_password is not None:
            if self.current_password is None:
                raise ValueError('current_password is needed to update new password')

            if self.new_password != self.new_repeat_password:
                raise ValueError('new_password and new_repeat_password do not match')

        return self
