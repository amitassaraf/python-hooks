from typing import Any, Callable, Optional, Tuple, Union

from .use import use_state


def __dispatch_factory(
    reducer: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]],
    state: Optional[dict[str, Any]],
    set_state: Callable[[dict[str, Any]], Any],
    middleware: Union[
        list[
            Callable[
                [dict[str, Any], Callable[[Any], Any], dict[str, Any]], dict[str, Any]
            ]
        ],
        None,
    ] = None,
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """
    Create a dispatch function for a reducer.
    :param reducer: The reducer to use
    :param state: The state to use
    :param set_state: The set_state function to use
    :param middleware: The middleware to use
    :return: The dispatch function
    """
    if middleware is None:
        middleware = []

    def dispatch(action: dict[str, Any]) -> dict[str, Any]:
        """
        Dispatch an action to the reducer. The action will be passed to the middleware. The middleware will be called
        in order. The last middleware will call the reducer. The reducer will return the new state. The new state will
        be set.
        :param action: The action to dispatch
        :return: The new state
        """
        inner_middleware = middleware

        new_state: dict[str, Any] = state

        if inner_middleware is None:
            inner_middleware = []
        inner_middleware.append(
            lambda inner_state, _, inner_action: reducer(inner_state, inner_action)
        )

        def runner(state, middlewares, action):
            current = middlewares.pop(0)
            return current(
                state,
                lambda inner_state, inner_action: runner(
                    inner_state, middlewares, inner_action
                ),
                action,
            )

        state_change: dict[str, Any] = runner(new_state, inner_middleware, action)
        new_state = {**new_state, **state_change}
        set_state(new_state)
        return new_state

    return dispatch


def use_reducer(
    reducer: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]],
    initial_state: Optional[dict[str, Any]] = None,
    middleware: Union[
        list[
            Callable[
                [dict[str, Any], Callable[[Any], Any], dict[str, Any]], dict[str, Any]
            ]
        ],
        None,
    ] = None,
) -> tuple[dict[str, Any], Callable[[dict[str, Any]], dict[str, Any]]]:
    """
    Create a reducer hook. The reducer will be called when the dispatch function is called.
    :param reducer: The reducer to use
    :param initial_state: The initial state to use
    :param middleware: The middlewares to use in order, if any
    :return: The state and the dispatch function
    """
    state, set_state = use_state(initial_state)
    return state, __dispatch_factory(reducer, state, set_state, middleware or [])
