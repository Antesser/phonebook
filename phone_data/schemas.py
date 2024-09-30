from pydantic import BaseModel


class PhoneAndAddress(BaseModel):
    phone: str
    address: str


class UpdatePhoneAndAddress(BaseModel):
    phone: str | None = None
    address: str | None = None
