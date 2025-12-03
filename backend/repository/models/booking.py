from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy import true
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend.repository.models.base import Base
from backend.repository.models.company import Company
from backend.repository.models.client import Client
from backend.repository.models.mixins import CreatedAtMixin, UpdatedAtMixin


class Booking(CreatedAtMixin, UpdatedAtMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    time_start: Mapped[datetime] = mapped_column()
    time_end: Mapped[datetime] = mapped_column()
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
        nullable=False,
    )
