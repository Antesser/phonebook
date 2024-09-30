from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from phone_data.schemas import PhoneAndAddress

router = APIRouter(prefix="", tags=["phones"])


@router.get("/check_data")
async def get_address_data(request: Request, phone: str):
    # using our state client to work with redis connection
    redis_client = request.app.state.redis_client
    value = await redis_client.get_value(phone)
    if value is not None:
        value = value.decode("utf-8")
        return JSONResponse(dict(address=value))
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Such number is missing in DB: {phone}",
        )


@router.post("/write_data")
async def write_phone_and_address(request: Request, data: PhoneAndAddress):
    redis_client = request.app.state.redis_client

    await redis_client.insert_data(data.phone, data.address)
    return JSONResponse(dict(response=f"DB has been added with {data}"))


@router.patch("/write_data")
async def update_address(request: Request, data: PhoneAndAddress):
    redis_client = request.app.state.redis_client
    value = await redis_client.get_value(data.phone)
    if value is not None:
        await redis_client.insert_data(data.phone, data.address)
        return JSONResponse(dict(response=f"DB has been updated with {data}"))
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Such number is missing in DB: {data.phone}",
        )
