from backend.entity.company import CompanyEntity
from backend.repository.models.base import Base
from backend.repository.models.mixins import CreatedAtMixin, UpdatedAtMixin

from sqlalchemy import String, Text
from sqlalchemy import true
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Token(CreatedAtMixin, UpdatedAtMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    access_token: Mapped[str] = mapped_column(unique=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)
