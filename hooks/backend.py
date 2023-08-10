from types import SimpleNamespace
from typing import Any, TypeVar, Union

import threading
from functools import lru_cache

# Extend pickle to support lambdas
import dill as pickle

thread_local = threading.local()
T = TypeVar("T")
BACKEND_KEY = "__hooks_backend__"


class HooksBackend(SimpleNamespace):
    @classmethod
    def load(cls, identifier: str) -> Any:
        raise NotImplemented

    @classmethod
    def save(cls, identifier: str, value: Any) -> Union[bool, None, Any]:
        raise NotImplemented

    @classmethod
    def exists(cls, identifier: str) -> bool:
        raise NotImplemented

    @classmethod
    def reset_backend(cls) -> None:
        raise NotImplemented


class PickleHooksBackend(HooksBackend):
    @classmethod
    def load(cls, identifier: str) -> Any:
        return pickle.loads(getattr(thread_local, BACKEND_KEY + identifier))

    @classmethod
    def save(cls, identifier: str, value: Any) -> bool:
        setattr(thread_local, BACKEND_KEY + identifier, pickle.dumps(value))
        return True

    @classmethod
    def exists(cls, identifier: str) -> bool:
        return hasattr(thread_local, BACKEND_KEY + identifier)

    @classmethod
    def reset_backend(cls) -> None:
        keys = []
        for key, value in thread_local.__dict__:  # type: ignore
            if key.startswith(BACKEND_KEY):  # type: ignore
                keys.append(key)  # type: ignore
        for key in keys:
            del thread_local.__dict__[key]


@lru_cache(maxsize=None)
def python_object_backend_factory(wrapped_cls: type[T]) -> type[HooksBackend]:
    class PythonObjectHooksBackend(HooksBackend):
        @classmethod
        def load(cls, identifier: str) -> Any:
            return getattr(wrapped_cls, identifier)

        @classmethod
        def save(cls, identifier: str, value: Any) -> bool:
            setattr(wrapped_cls, identifier, value)
            return True

        @classmethod
        def exists(cls, identifier: str) -> bool:
            return hasattr(wrapped_cls, identifier)

    return PythonObjectHooksBackend


def set_hooks_backend(backend: type[HooksBackend]) -> None:
    setattr(thread_local, BACKEND_KEY, backend)


def get_hooks_backend() -> Any:
    return getattr(thread_local, BACKEND_KEY, PickleHooksBackend)
