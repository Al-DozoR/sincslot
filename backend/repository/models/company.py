from backend.entity.company import CompanyEntity
from backend.repository.models.base import Base
from backend.repository.models.mixins import CreatedAtMixin, UpdatedAtMixin

from sqlalchemy import String, Text
from sqlalchemy import true
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Company(CreatedAtMixin, UpdatedAtMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    address: Mapped[str] = mapped_column(String(255), unique=False)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    phone: Mapped[str] = mapped_column(String(255), unique=True)
    hash_password: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
    )
    access_token: Mapped[str] = mapped_column(unique=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)

    @classmethod
    def to_company_model(cls, obj: CompanyEntity):
        return cls(
            name=obj.name,
            description=obj.description,
            address=obj.address,
            email=obj.email,
            phone=obj.phone,
            hash_password=obj.password,
            updated_at=obj.updated_at,
            created_at=obj.created_at,
        )

    def __str__(self):
        return self.name
