from types import SimpleNamespace
from typing import Any, TypeVar

import threading
from functools import lru_cache

import dill as pickle

thread_local = threading.local()
T = TypeVar("T")
STORE_KEY = "__hooksStore"


class Store(SimpleNamespace):
    @staticmethod
    def load(identifier: str) -> Any:
        raise NotImplemented

    @staticmethod
    def save(identifier: str, value: Any) -> bool:
        raise NotImplemented

    @staticmethod
    def exists(identifier: str) -> bool:
        raise NotImplemented

    @staticmethod
    def reset_store():
        raise NotImplemented


class PickleStore(Store):
    @staticmethod
    def load(identifier: str) -> Any:
        return pickle.loads(getattr(thread_local, STORE_KEY + identifier))

    @staticmethod
    def save(identifier: str, value: Any) -> bool:
        setattr(thread_local, STORE_KEY + identifier, pickle.dumps(value))
        return True

    @staticmethod
    def exists(identifier: str) -> bool:
        return hasattr(thread_local, STORE_KEY + identifier)

    @staticmethod
    def reset_store():
        keys = []
        for key, value in thread_local.__dict__:
            if key.startswith(STORE_KEY):
                keys.append(key)
        for key in keys:
            del thread_local.__dict__[key]


@lru_cache(maxsize=None)
def python_object_store_factory(wrapped_cls: type[T]) -> type[Store]:
    class PythonObjectStore(Store):
        @staticmethod
        def load(identifier: str) -> Any:
            return getattr(wrapped_cls, identifier)

        @staticmethod
        def save(identifier: str, value: Any) -> bool:
            setattr(wrapped_cls, identifier, value)
            return True

        @staticmethod
        def exists(identifier: str) -> bool:
            return hasattr(wrapped_cls, identifier)

    return PythonObjectStore


def _set_current_store(store: type[Store]):
    setattr(thread_local, STORE_KEY, store)


def _get_current_store() -> type[Store]:
    return getattr(thread_local, STORE_KEY, PickleStore)
