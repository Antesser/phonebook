import re
from pydantic import BaseModel, field_validator


class PhoneAndAddress(BaseModel):
    phone: str
    address: str

    @field_validator("phone", mode="before")
    def phone_validation(cls, number):
        regex = r"^[1-9][0-9\-\(\)\.]{9,15}$"
        if number and not re.search(regex, number, re.I):
            raise ValueError("Phone Number Invalid.")
        return number
