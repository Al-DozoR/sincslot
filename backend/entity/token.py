from typing import Optional
from dataclasses import dataclass, field


@dataclass
class TokenEntity:
    access_token: str
    refresh_token: str
    id: Optional[int] = field(default=None)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def to_model(cls, dict_obj):
        return cls(**dict_obj)