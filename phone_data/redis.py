from phone_data.logger import logging
import redis.asyncio as redis


class Redis:
    redis_client: redis.Redis = None

    @classmethod
    async def connect(
        cls,
        host: str = "localhost",
        port: int = 6379,
        username=None,
        password=None,
    ):
        try:
            # Connect to Redis server
            cls.redis_client = redis.Redis(
                host=host, port=port, username=username, password=password
            )
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

    # @classmethod
    # async def check_key(cls, key: str):
    #     result = await cls.redis_client.exists(key)
    #     return result


