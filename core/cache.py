from functools import lru_cache


@lru_cache(maxsize=1024)
def cached_call(key: str, value_factory):
    return value_factory()
