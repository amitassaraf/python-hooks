from typing import Any, Callable

from collections.abc import Awaitable

from box import Box

from hooks.asyncio.reducers import use_reducer

global _redux_root_reducer


async def create_redux_store(
    reducer: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]],
    initial_state: dict[str, Any],
) -> None:
    """
    Initialize the redux store. This must be called before any other redux functions are used.
    :param reducer: The reducer to use
    :param initial_state: The initial state to use
    :return: None
    """
    global _redux_root_reducer
    await use_reducer(reducer, initial_state, [])
    _redux_root_reducer = reducer


async def use_selector(callable: Callable[[dict[str, Any]], Any]) -> Any:
    """
    Use a selector to get a value from the redux store.
    :param callable: The selector to use
    :return: The value from the selector
    """
    global _redux_root_reducer
    if not _redux_root_reducer:
        raise Exception("Redux store not initialized")

    state, _ = await use_reducer(_redux_root_reducer)
    return callable(Box(state))


async def use_dispatch() -> Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]:
    """
    Get the dispatch function from the redux store.
    :return: The dispatch function
    """
    global _redux_root_reducer
    if not _redux_root_reducer:
        raise Exception("Redux store not initialized")

    _, dispatch = await use_reducer(_redux_root_reducer)
    return dispatch
