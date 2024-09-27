import os

from dotenv import load_dotenv

load_dotenv()

redis_host = os.environ["REDIS_HOST"]
redis_port = os.environ["REDIS_PORT"]
