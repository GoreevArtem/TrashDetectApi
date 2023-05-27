from redis import asyncio as aioredis
from settings.settings import settings

path = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
redis = aioredis.from_url(path)