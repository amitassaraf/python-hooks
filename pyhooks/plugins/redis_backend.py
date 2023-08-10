from typing import Any

from pyhooks.backend import HooksBackend

try:
    # Extend pickle to support lambdas
    import dill as pickle
    import redis

    class RedisHooksBackend(HooksBackend):
        redis_client = None

        @classmethod
        def initialize(cls, host: str, port: int, **kwargs):
            cls.redis_client = redis.Redis(host=host, port=port, decode_responses=True)

        @classmethod
        def load(cls, identifier: str) -> Any:
            return pickle.loads(cls.redis_client.get(identifier))

        @classmethod
        def save(cls, identifier: str, value: Any) -> bool:
            return cls.redis_client.set(identifier, pickle.dumps(value))

        @classmethod
        def exists(cls, identifier: str) -> bool:
            return cls.redis_client.exists(identifier)

        @classmethod
        def reset_backend(cls):
            for key in cls.redis_client.scan_iter("*"):
                cls.redis_client.delete(key)

except ImportError:
    raise ImportError("Redis backend requires redis to be installed")
