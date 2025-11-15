from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from backend.core.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        converts CamelCase to snake_case
        """
        chars = []
        for c_idx, char in enumerate(cls.__name__):
            if c_idx and char.isupper():
                nxt_idx = c_idx + 1
                flag = nxt_idx >= len(cls.__name__) or cls.__name__[nxt_idx].isupper()
                prev_char = cls.__name__[c_idx - 1]
                if prev_char.isupper() and flag:
                    pass
                else:
                    chars.append("_")
            chars.append(char.lower())
        return "".join(chars)
