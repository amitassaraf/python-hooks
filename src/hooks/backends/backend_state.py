from typing import Any, Optional

from .async_interface import AsyncHooksBackend
from .memory_backend import MemoryBackend as DefaultHooksBackend

BACKEND_KEY = "__hooks_backend__"


def set_hooks_backend(backend: type) -> None:
    globals()[BACKEND_KEY] = backend


def get_hooks_backend(using_async: Optional[bool] = False) -> Any:
    backend = globals().get(BACKEND_KEY, DefaultHooksBackend)
    if using_async and not issubclass(backend, AsyncHooksBackend):
        raise Exception("You cannot use async hooks with a non-async backend")
    return backend
