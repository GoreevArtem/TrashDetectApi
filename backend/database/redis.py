import redis

from settings.settings import settings

redis_startup = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
