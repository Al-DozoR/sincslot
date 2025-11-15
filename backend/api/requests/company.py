from pydantic import BaseModel
from typing import Optional


class CreateCompany(BaseModel):
    name: str
    address: Optional[str] = None
    email: str
    phone: Optional[str] = None
    password: str
    repeat_password: str