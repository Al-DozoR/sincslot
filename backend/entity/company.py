from typing import Optional
from dataclasses import dataclass, field


@dataclass
class CompanyEntity:
    name: str
    email: str
    password: str
    phone: str
    updated_at: Optional[int] = field(default=None)
    created_at: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)
    address: Optional[str] = field(default=None)
    id: Optional[int] = field(default=None)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def to_model(cls, dict_obj):
        return cls(**dict_obj)
