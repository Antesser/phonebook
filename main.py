from contextlib import asynccontextmanager
from phone_data.router import router as phone_data_router
from fastapi import FastAPI
from phone_data.logger import logging

from phone_data.redis import Redis


async def run_redis():
    await Redis.connect()
    return Redis


async def stop_redis():
    await Redis.close()
    return Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.debug("enter lifespan")
    # В контексте FastAPI app.state — это механизм для хранения и извлечения данных между запросами в рамках одного сеанса (соединения). Это позволяет сохранять состояние приложения, например, аутентифицированного пользователя или какие-либо настройки.
    # В Python объект app является экземпляром класса FastAPI, который предоставляет различные методы и атрибуты для создания веб-сервиса. Метод state() используется для работы с данными, которые должны быть доступны на протяжении всего времени жизни запроса.
    app.state.redis_client = await run_redis()
    yield
    app.state.redis_client = await stop_redis()
    logging.debug("exit lifespan")


app = FastAPI(lifespan=lifespan)


app.include_router(phone_data_router)
