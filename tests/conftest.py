from typing import Any

import asyncio

# Extend pickle to support lambdas
import dill as pickle
import pytest

from hooks.backends.async_interface import AsyncHooksBackend
from hooks.backends.memory_backend import MemoryBackend


@pytest.fixture()
async def async_backend():
    BACKEND_KEY = "__hooks_backend__"

    class AsyncMemoryBackend(AsyncHooksBackend):
        @classmethod
        async def load(cls, identifier: str) -> Any:
            return pickle.loads(globals().get(BACKEND_KEY + identifier))

        @classmethod
        async def save(cls, identifier: str, value: Any) -> bool:
            globals()[BACKEND_KEY + identifier] = pickle.dumps(value)
            return True

        @classmethod
        async def exists(cls, identifier: str) -> bool:
            return BACKEND_KEY + identifier in globals()

        @classmethod
        async def reset_backend(cls) -> None:
            keys = []
            for key, value in globals().items():
                if key.startswith(BACKEND_KEY):
                    keys.append(key)
            for key in keys:
                del globals()[key]

    await AsyncMemoryBackend.use()
    yield
    MemoryBackend.use()
