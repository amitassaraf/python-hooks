from typing import Any

from .memory_backend import MemoryBackend as DefaultHooksBackend

BACKEND_KEY = "__hooks_backend__"


def set_hooks_backend(backend: type) -> None:
    globals()[BACKEND_KEY] = backend


def get_hooks_backend() -> Any:
    return globals().get(BACKEND_KEY, DefaultHooksBackend)
