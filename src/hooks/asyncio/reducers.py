from typing import Any, Callable, Dict, Optional, Union

from collections.abc import Awaitable, Coroutine
from functools import wraps

from ..backends.backend_state import get_hooks_backend
from ..utils import alambda


def __async_dispatch_factory(
    reducer: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]],
    state_fetcher: Callable[[], dict[str, Any]],
    set_state: Callable[[dict[str, Any]], Any],
    middleware: Union[
        list[
            Callable[
                [dict[str, Any], Callable[[Any], Any], dict[str, Any]], dict[str, Any]
            ]
        ],
        None,
    ] = None,
) -> Callable[[dict[str, Any]], Coroutine[Any, Any, dict[str, Any]]]:
    """
    Create a dispatch function for a reducer.
    :param reducer: The reducer to use
    :param state_fetcher: The state_fetcher to use
    :param set_state: The set_state function to use
    :param middleware: The middleware to use
    :return: The dispatch function
    """
    if middleware is None:
        middleware = []

    async def dispatch(action: dict[str, Any]) -> dict[str, Any]:
        """
        Dispatch an action to the reducer. The action will be passed to the middleware. The middleware will be called
        in order. The last middleware will call the reducer. The reducer will return the new state. The new state will
        be set.
        :param action: The action to dispatch
        :return: The new state
        """
        inner_middleware = middleware

        new_state: dict[str, Any] = state_fetcher()

        if inner_middleware is None:
            inner_middleware = []

        async def reducer_wrapper(inner_state, _, inner_action):
            return reducer(inner_state, inner_action)

        inner_middleware.append(reducer_wrapper)

        async def runner(state, middlewares, action):
            current = middlewares.pop(0)
            return await current(
                state,
                lambda inner_state, inner_action: alambda(
                    await runner(inner_state, middlewares, inner_action) for _ in "_"
                ),
                action,
            )

        state_change: dict[str, Any] = await runner(new_state, inner_middleware, action)
        new_state = {**new_state, **state_change}
        await set_state(new_state)
        return new_state

    return dispatch


async def use_reducer(
    reducer: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]],
    initial_state: Optional[dict[str, Any]] = None,
    middleware: Union[
        list[
            Callable[
                [dict[str, Any], Callable[[Any], Any], dict[str, Any]],
                Awaitable[dict[str, Any]],
            ]
        ],
        None,
    ] = None,
) -> tuple[dict[str, Any], Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]]:
    """
    Create a reducer hook. The reducer will be called when the dispatch function is called.
    :param reducer: The reducer to use
    :param initial_state: The initial state to use
    :param middleware: The middlewares to use in order, if any
    :return: The state and the dispatch function
    """
    _backend = get_hooks_backend(using_async=True)
    identifier = reducer.__module__ + (reducer.__qualname__ or reducer.__name__)

    async def state_wrapper(value) -> None:
        state_wrapper.val = value
        await _backend.save(identifier, value)

    def state_fetcher() -> dict[str, Any]:
        return state_wrapper.val

    if (await _backend.exists(identifier)) is True:
        loaded_value = await _backend.load(identifier)
        state_wrapper.val = loaded_value
        return state_wrapper.val, __async_dispatch_factory(
            reducer, state_fetcher, state_wrapper, middleware or []
        )

    await state_wrapper(initial_state)
    return state_wrapper.val, __async_dispatch_factory(
        reducer, state_fetcher, state_wrapper, middleware or []
    )


def combine_reducers(
    *reducers: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
):
    """
    Combine multiple reducers into one reducer.
    :param reducers: The reducers to combine
    :return: The combined reducer
    """

    @wraps(reducers[0])
    def combined_reducer(
        state: dict[str, Any], action: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Combine multiple reducers into one reducer.
        :param state: The state to use
        :param action: The action to use
        :return: The new state
        """
        new_state = state
        for reducer in reducers:
            new_state = reducer(new_state, action)
        return new_state

    return combined_reducer
