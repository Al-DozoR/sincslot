from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class AccessTokenEntity:
    company_id: int
    exp: int
    type: str

    def to_dict(self):
        return self.__dict__

    @classmethod
    def to_model(cls, dict_obj):
        return cls(**dict_obj)


@dataclass
class RefreshTokenEntity:
    company_id: int
    exp: int
    type: str

    def to_dict(self):
        return self.__dict__

    @classmethod
    def to_model(cls, dict_obj):
        return cls(**dict_obj)


@dataclass
class TokenEntity:
    access_token: str
    refresh_token: str
    is_revoke: bool
    id: Optional[int] = field(default=None)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def to_model(cls, dict_obj):
        return cls(**dict_obj)
