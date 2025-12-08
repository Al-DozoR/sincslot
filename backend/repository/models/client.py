from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from backend.repository.models.base import Base
from backend.repository.models.mixins import CreatedAtMixin, UpdatedAtMixin
from backend.entity.client import ClientEntity


if TYPE_CHECKING:
    from .booking import Booking


class Client(CreatedAtMixin, UpdatedAtMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    phone: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    bookings: Mapped[list["Booking"]] = relationship(back_populates="client")

    def to_client_entity(self) -> ClientEntity:
        return ClientEntity(
            id=self.id,
            name=self.name,
            phone=self.phone,
            updated_at=int(self.updated_at.timestamp()),
            created_at=int(self.created_at.timestamp()),
        )
