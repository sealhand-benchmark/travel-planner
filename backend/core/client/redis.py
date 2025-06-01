from redis.asyncio import Redis
from core.config import env

redis_client = Redis.from_url(url=env.REDIS_HOST)
