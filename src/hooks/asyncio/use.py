# mypy: ignore-errors
from typing import Any, Callable, Optional, TypeVar

import inspect
from collections.abc import Coroutine

from ..backends.backend_state import get_hooks_backend
from ..frame_utils import __identify_hook_and_backend

T = TypeVar("T")


async def use_state(default_value: T) -> tuple[T, Callable[[Any], Any]]:
    """
    Create a stateful hook.
    :param default_value: The default value of the state
    :return: The current value of the state and a function to update the state
    """
    identifier, _backend = __identify_hook_and_backend(using_async=True)

    async def state_wrapper(value: T) -> None:
        state_wrapper.val = value
        await _backend.save(identifier, value)

    exists = await _backend.exists(identifier)
    if exists is True:
        loaded_value = await _backend.load(identifier)
        state_wrapper.val = loaded_value
        return state_wrapper.val, state_wrapper

    await state_wrapper(default_value)
    return state_wrapper.val, state_wrapper


async def use_effect(
    callback: Optional[Callable[[], Any]] = None,
    dependencies: Optional[list[Any]] = None,
) -> Optional[Callable[[Callable[[], Any]], Coroutine[Any, Any, Callable[[], None]]]]:
    """
    Create an effect hook. The callback will be called when the dependencies change.
    :param callback: The callback to call when the dependencies change
    :param dependencies: The dependencies to watch for changes
    :param decorating: Whether the use_effect hook is currently used as a decorator
    :return: None
    """
    saved_dependencies, set_dependencies = await use_state(dependencies or [])
    has_ran, set_initial_ran = await use_state(False)
    if saved_dependencies != dependencies or not has_ran:
        await set_dependencies(dependencies)
        await set_initial_ran(True)
        if inspect.iscoroutinefunction(callback):
            await callback()
        else:
            callback()
    return


async def use_memo(callback: Callable[[], Any], dependencies: list[Any]) -> Any:
    """
    Create a memoized hook. The callback will be called when the dependencies change. Practically it is an alias for
    use_effect.
    :param callback: The callback to call when the dependencies change
    :param dependencies: The dependencies to watch for changes
    :return: The return value of the callback
    """
    return use_effect(callback, dependencies)


async def create_context(default_value: Any) -> str:
    """
    Create a context hook.
    :param default_value: The default value of the context
    :return: The identifier of the context
    """
    identifier, _backend = __identify_hook_and_backend(
        always_global_backend=True, prefix="__hooks_context__", using_async=True
    )
    if (await _backend.exists(identifier)) is False:
        await _backend.save(identifier, default_value)
    return identifier


async def set_context_value(context: Any, value: Any) -> str:
    """
    Set the value of a context hook. The value will be saved in the backend.
    :param context: The identifier of the context
    :param value: The value to set
    :return: The value that was set
    """
    _backend = get_hooks_backend(using_async=True)
    await _backend.save(context, value)
    return value


async def use_context(context: Any) -> Any:
    """
    Create a context hook. The value of the context will be loaded from the backend.
    :param context: The identifier of the context
    :return: The value of the context
    """
    _backend = get_hooks_backend(using_async=True)
    return await _backend.load(context)
