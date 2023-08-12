from typing import Any, TypeVar

import threading

# Extend pickle to support lambdas
import dill as pickle

from .interface import HooksBackend

T = TypeVar("T")
threading_local = threading.local()
BACKEND_KEY = "__hooks_backend__"


class ThreadsafeBackend(HooksBackend):
    @classmethod
    def load(cls, identifier: str) -> Any:
        return pickle.loads(getattr(threading_local, BACKEND_KEY + identifier, None))

    @classmethod
    def save(cls, identifier: str, value: Any) -> bool:
        setattr(threading_local, BACKEND_KEY + identifier, pickle.dumps(value))
        return True

    @classmethod
    def exists(cls, identifier: str) -> bool:
        return hasattr(threading_local, BACKEND_KEY + identifier)

    @classmethod
    def reset_backend(cls) -> None:
        keys = []
        for key, value in threading_local.__dict__.items():
            if key.startswith(BACKEND_KEY):
                keys.append(key)
        for key in keys:
            del threading_local.__dict__[key]
