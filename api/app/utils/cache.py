import redis
from fastapi_cache import caches
from fastapi_cache.backends.redis import CACHE_KEY

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def redis_cache():
    return caches.get(CACHE_KEY)
