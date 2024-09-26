from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from phone_data.schemas import PhoneAndAddress

router = APIRouter(prefix="", tags=["phones"])


@router.get("/check_data")
async def get_address_data(request: Request, phone: str):
    redis_client = request.app.state.redis_client
    value = await redis_client.get_value(phone)
    if value is not None:
        value = value.decode("utf-8")
        return JSONResponse(dict(address=value))
    else:
        return {"Such number is missing in DB": phone}


@router.post("/write_data")
async def write_phone_or_address(request: Request, data: PhoneAndAddress):
    redis_client = request.app.state.redis_client
    # print(await redis_client.check_key(data.phone))
    # if await redis_client.check_key(data.phone) !=0:
    await redis_client.insert_data(data.phone, data.address)
    return JSONResponse(dict(response=f"DB has been updated with {data}"))
