from typing import Annotated, Union

import phonenumbers
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from pydantic import BaseModel

E164NumberType = Annotated[
    Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(number_format="E164")
]


class ClientRegisterRequest(BaseModel):
    name: str
    phone: E164NumberType


class ClientLoginRequest(BaseModel):
    phone: E164NumberType
