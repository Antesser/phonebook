from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from config import amount_of_phone_numbers
from phone_data.schemas import PhoneAndAddress, UpdatePhoneAndAddress

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
            detail="Such number is missing in DB: {data.phone}",
        )


@router.post("/write_data")
async def write_phone_or_address(request: Request, data: PhoneAndAddress):
    redis_client = request.app.state.redis_client
    try:
        # some basic checks if inputed data is sort of a phone number
        if (
            isinstance(int(data.phone), int)
            and len(data.phone) == amount_of_phone_numbers
        ):
            await redis_client.insert_data(data.phone, data.address)
            return JSONResponse(
                dict(response=f"DB has been added with {data}")
            )
        else:
            return JSONResponse(
                dict(response=f"Check amount of numbers in phone={data.phone}")
            )
    except ValueError:
        return JSONResponse(
            dict(
                response=f"Phone={data.phone} doesn't look like a number, kindly provide a proper one"
            )
        )


@router.patch("/write_data")
async def update_address(
    request: Request, data: UpdatePhoneAndAddress
):
    redis_client = request.app.state.redis_client
    try:
        if (
            isinstance(int(data.phone), int)
            and len(data.phone) == amount_of_phone_numbers
        ):
            value = await redis_client.get_value(data.phone)
            if value is not None:
                await redis_client.insert_data(data.phone, data.address)
                return JSONResponse(
                    dict(response=f"DB has been updated with {data}")
                )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Such number is missing in DB: {data.phone}",
                )
        else:
            return JSONResponse(
                dict(response=f"Check amount of numbers in phone={data.phone}")
            )
    except ValueError:
        return JSONResponse(
            dict(
                response=f"Phone={data.phone} doesn't look like a number, kindly provide a proper one"
            )
        )
