from typing import Any, Callable

from hooks import use_state


def __dispatch_factory(
    reducer: Callable[[dict, dict], dict],
    state: dict,
    set_state: Callable[[dict], Any],
    middleware: list[Callable[[dict, Callable, dict], dict]] = None,
) -> Callable[[dict], dict]:
    """
    Create a dispatch function for a reducer.
    :param reducer: The reducer to use
    :param state: The state to use
    :param set_state: The set_state function to use
    :param middleware: The middleware to use
    :return: The dispatch function
    """

    def dispatch(action: dict) -> dict:
        """
        Dispatch an action to the reducer. The action will be passed to the middleware. The middleware will be called
        in order. The last middleware will call the reducer. The reducer will return the new state. The new state will
        be set.
        :param action: The action to dispatch
        :return: The new state
        """
        new_state: dict = state
        middleware.append(
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

        state_change: dict = runner(new_state, middleware, action)
        new_state = {**new_state, **state_change}
        set_state(new_state)
        return new_state

    return dispatch


def use_reducer(
    reducer: Callable[[dict, dict], dict],
    initial_state: dict,
    middleware: list[Callable[[dict, Callable, dict], dict]],
) -> (dict, Callable[[dict], dict]):
    """
    Create a reducer hook. The reducer will be called when the dispatch function is called.
    :param reducer: The reducer to use
    :param initial_state: The initial state to use
    :param middleware: The middlewares to use in order, if any
    :return: The state and the dispatch function
    """
    state, set_state = use_state(initial_state)
    return state, __dispatch_factory(reducer, state, set_state, middleware)
