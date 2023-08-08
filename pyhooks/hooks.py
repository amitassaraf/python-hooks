from typing import Any, Callable, Tuple, TypeVar

from frame_utils import __identify_hook_and_store
from store import _get_current_store

T = TypeVar("T")


def use_state(default_value: T) -> tuple[T, Callable]:
    """
    Create a stateful hook.
    :param default_value: The default value of the state
    :return: The current value of the state and a function to update the state
    """
    identifier, _store = __identify_hook_and_store()

    def state_wrapper(value: T):
        state_wrapper.val = value
        _store.save(identifier, value)

    if _store.exists(identifier):
        loaded_value = _store.load(identifier)
        state_wrapper.val = loaded_value
        return state_wrapper.val, state_wrapper

    state_wrapper(default_value)
    return state_wrapper.val, state_wrapper


def use_effect(callback: Callable, dependencies: list):
    """
    Create an effect hook. The callback will be called when the dependencies change.
    :param callback: The callback to call when the dependencies change
    :param dependencies: The dependencies to watch for changes
    :return: None
    """
    saved_dependencies, set_dependencies = use_state(dependencies)
    has_ran, set_initial_ran = use_state(False)
    if saved_dependencies != dependencies or not has_ran:
        set_dependencies(dependencies)
        set_initial_ran(True)
        callback()
    return


def use_memo(callback: Callable, dependencies: list):
    """
    Create a memoized hook. The callback will be called when the dependencies change. Practically it is an alias for
    use_effect.
    :param callback: The callback to call when the dependencies change
    :param dependencies: The dependencies to watch for changes
    :return: The return value of the callback
    """
    return use_effect(callback, dependencies)


def create_context(default_value: Any) -> str:
    """
    Create a context hook.
    :param default_value: The default value of the context
    :return: The identifier of the context
    """
    identifier, _store = __identify_hook_and_store(always_global_store=True)
    _store.save(identifier, default_value)
    return identifier


def set_context_value(context: Any, value: Any) -> str:
    """
    Set the value of a context hook. The value will be saved in the store.
    :param context: The identifier of the context
    :param value: The value to set
    :return: The value that was set
    """
    _store = _get_current_store()
    _store.save(context, value)
    return value


def use_context(context: Any) -> Any:
    """
    Create a context hook. The value of the context will be loaded from the store.
    :param context: The identifier of the context
    :return: The value of the context
    """
    _store = _get_current_store()
    return _store.load(context)
