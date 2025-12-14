from typing import Optional
from enum import StrEnum
from datetime import datetime
from dataclasses import dataclass, field


class BookingStatus(StrEnum):
    pending: str = "pending"
    approved: str = "approved"
    cancelled: str = "cancelled"


@dataclass
class BookingEntity:
    service_id: int
    client_id: int
    time_start: datetime
    time_end: datetime
    is_active: bool
    status: BookingStatus = field(default=BookingStatus.pending)
    id: Optional[int] = field(default=None)
    updated_at: Optional[int] = field(default=None)
    created_at: Optional[int] = field(default=None)
