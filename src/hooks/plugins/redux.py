from typing import Any, Callable

from box import Box

from hooks import use_reducer

global _redux_root_reducer


def create_redux_store(
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
    use_reducer(reducer, initial_state, [])
    _redux_root_reducer = reducer


def use_selector(callable: Callable[[dict[str, Any]], Any]) -> Any:
    """
    Use a selector to get a value from the redux store.
    :param callable: The selector to use
    :return: The value from the selector
    """
    global _redux_root_reducer
    if not _redux_root_reducer:
        raise Exception("Redux store not initialized")

    state, _ = use_reducer(_redux_root_reducer)
    return callable(Box(state))


def use_dispatch() -> Callable[[dict[str, Any]], dict[str, Any]]:
    """
    Get the dispatch function from the redux store.
    :return: The dispatch function
    """
    global _redux_root_reducer
    if not _redux_root_reducer:
        raise Exception("Redux store not initialized")

    _, dispatch = use_reducer(_redux_root_reducer)
    return dispatch
