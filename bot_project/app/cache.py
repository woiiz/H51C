import time
from app.config import CACHE_TTL

_cache = {}

def get_cached_extraction(host_id: str):
    if host_id in _cache:
        data, timestamp = _cache[host_id]
        if time.time() - timestamp < CACHE_TTL:
            return data
        else:
            del _cache[host_id]
    return None

def set_cached_extraction(host_id: str, data: dict):
    _cache[host_id] = (data, time.time())
