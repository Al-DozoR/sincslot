from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ClientEntity:
    name: str
    phone: str
    id: Optional[int] = field(default=None)
    updated_at: Optional[int] = field(default=None)
    created_at: Optional[int] = field(default=None)
