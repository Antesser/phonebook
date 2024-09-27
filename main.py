from contextlib import asynccontextmanager

from fastapi import FastAPI

from phone_data.logger import logging
from phone_data.redis import Redis
from phone_data.router import router as phone_data_router


async def run_redis():
    await Redis.connect()
    return Redis


async def stop_redis():
    await Redis.close()
    return Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # as on_event is deprecated i'm using lifespan to establish db conn once before starting an app and shut it down afterwards
    logging.debug("enter lifespan")
    # app.state is a mechanism for storing and retrieving data between requests within a single session (connection), meaning
    # state method is used to work with data that should be available throughout the lifetime of the request.
    app.state.redis_client = await run_redis()
    yield
    app.state.redis_client = await stop_redis()
    logging.debug("exit lifespan")


app = FastAPI(lifespan=lifespan)


app.include_router(phone_data_router)
