from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum


class DaysOfWeek(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7

    @staticmethod
    def to_dict() -> dict:
        return {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7,
        }


@dataclass
class WorkSchedule:
    day_of_week: DaysOfWeek
    work_start: datetime
    work_end: datetime

    def to_dict(self):
        return {
            "day_of_week": self.day_of_week.value,
            "work_start": self.work_start,
            "work_end": self.work_end,
        }


@dataclass
class CompanyEntity:
    name: str
    email: str
    password: str
    phone: str
    work_schedule: list[WorkSchedule] = field(default=None)
    file_path: str = field(default=None)
    updated_at: Optional[int] = field(default=None)
    created_at: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)
    address: Optional[str] = field(default=None)
    id: Optional[int] = field(default=None)

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def to_model(cls, dict_obj):
        return cls(**dict_obj)
