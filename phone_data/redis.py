import redis.asyncio as redis

from config import settings
from phone_data.logger import logging


class Redis:
    """Creating a client to connect and manage Redis"""

    redis_client: redis.Redis = None

    # ? on the other hand we could've created connection_pool and used Depends injections in endpoints to reduce open-closing connection costs
    @classmethod
    async def connect(
        cls,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
    ):
        try:
            cls.redis_client = redis.Redis(host=host, port=port)
        except redis.RedisError as e:
            logging.debug(f"Failed to connect to Redis: {e}")
            raise

        await cls.redis_client

    @classmethod
    async def close(cls):
        if cls.redis_client is not None:
            await cls.redis_client.aclose()

    @classmethod
    async def insert_data(cls, key: str, value: str):
        await cls.redis_client.set(key, value)

    @classmethod
    async def get_value(cls, key: str):
        result = await cls.redis_client.get(key)
        return result
