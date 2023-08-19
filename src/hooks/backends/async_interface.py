from types import SimpleNamespace
from typing import Any, TypeVar, Union

T = TypeVar("T")


class AsyncHooksBackend(SimpleNamespace):
    @classmethod
    async def use(cls, *args: Any, **kwargs: Any) -> Any:
        from .backend_state import set_hooks_backend

        set_hooks_backend(cls)
        return cls

    @classmethod
    async def load(cls, identifier: str) -> Any:
        raise NotImplemented

    @classmethod
    async def save(cls, identifier: str, value: Any) -> Union[bool, None, Any]:
        raise NotImplemented

    @classmethod
    async def exists(cls, identifier: str) -> bool:
        raise NotImplemented

    @classmethod
    async def reset_backend(cls) -> None:
        raise NotImplemented
