from pydantic import BaseModel


class PhoneAndAddress(BaseModel):
    phone: str
    address: str
