from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from backend.entity.company import DaysOfWeek


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


class CompanySuccessResponse(BaseModel):
    message: str


class CompanyErrorResponse(BaseModel):
    error: str


class CompanyRecoverPasswordResponse(BaseModel):
    pass


class CompanyWorkDay(BaseModel):
    day_of_week: DaysOfWeek = Field(default=DaysOfWeek.Monday)
    work_start: str = Field(examples=["9:00"], alias="workStart")
    work_end: str = Field(examples=["18:00"], alias="workEnd")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyWorkScheduleResponse(BaseModel):
    work_schedule: list[dict] = Field(alias="workSchedule")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyEntityResponse(BaseModel):
    id: int
    name: str
    email: str
    password: Optional[str] = None
    phone: str
    booking_url: str
    work_schedule: Optional[list[dict]] = Field(default=None, alias="workSchedule")
    filename: Optional[str] = None
    updated_at: Optional[int]= Field(default=None, alias="updatedAt")
    created_at: Optional[int] = Field(default=None, alias="createdAt")
    description: Optional[str] = None
    address: Optional[str] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
