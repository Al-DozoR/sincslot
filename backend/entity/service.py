from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ServiceEntity:
    name: str
    duration: int
    price: int
    company_id: int
    is_active: Optional[bool] = field(default=None)
    updated_at: Optional[int] = field(default=None)
    created_at: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)
    id: Optional[int] = field(default=None)

    def to_dict(self):
        return self.__dict__
