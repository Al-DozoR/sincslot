from backend.entity.token import TokenEntity
from backend.repository.models.base import Base
from backend.repository.models.mixins import CreatedAtMixin, UpdatedAtMixin

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Token(CreatedAtMixin, UpdatedAtMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    access_token: Mapped[str] = mapped_column(unique=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)

    @classmethod
    def to_token_model(cls, obj: TokenEntity):
        return cls(
            access_token=obj.access_token,
            refresh_token=obj.refresh_token,
        )
