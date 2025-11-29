from typing import Optional
from pydantic import BaseModel


class ServiceCreateRequest(BaseModel):
    name: str
    price: int
    duration: int
    description: Optional[str]
