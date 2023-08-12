from typing import Any, TypeVar

# Extend pickle to support lambdas
import dill as pickle

from .interface import HooksBackend

T = TypeVar("T")
BACKEND_KEY = "__hooks_backend__"


class MemoryBackend(HooksBackend):
    @classmethod
    def load(cls, identifier: str) -> Any:
        return pickle.loads(globals().get(BACKEND_KEY + identifier))

    @classmethod
    def save(cls, identifier: str, value: Any) -> bool:
        globals()[BACKEND_KEY + identifier] = pickle.dumps(value)
        return True

    @classmethod
    def exists(cls, identifier: str) -> bool:
        return BACKEND_KEY + identifier in globals()

    @classmethod
    def reset_backend(cls) -> None:
        keys = []
        for key, value in globals().items():
            if key.startswith(BACKEND_KEY):
                keys.append(key)
        for key in keys:
            del globals()[key]
