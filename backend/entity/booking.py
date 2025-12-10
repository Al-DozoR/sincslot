from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class BookingEntity:
    service_id: int
    client_id: int
    time_start: datetime
    time_end: datetime
    is_active: bool
    id: Optional[int] = field(default=None)
    updated_at: Optional[int] = field(default=None)
    created_at: Optional[int] = field(default=None)
