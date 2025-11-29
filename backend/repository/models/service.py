from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import true
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy  import CheckConstraint

from backend.repository.models.base import Base
from backend.repository.models.mixins import CreatedAtMixin, UpdatedAtMixin


class Service(CreatedAtMixin, UpdatedAtMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    price: Mapped[int] = mapped_column(Integer, CheckConstraint("price > 0", name="check_price_positive"))
    duration: Mapped[int] = mapped_column(Integer, CheckConstraint("duration > 0", name="check_price_positive"))
    description: Mapped[str] = mapped_column(
        String(255),
        default="",
        server_default="",
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
        nullable=False,
    )
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), nullable=True)
