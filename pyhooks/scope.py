from typing import Callable, Optional

from functools import wraps

HOOKED_FUNCTION_ATTRIBUTE = "__hooked_function__"

from contextlib import contextmanager


@contextmanager
def _hook_scope_manager(
    wrapped: Callable, limit_to_keys: Optional[list[str]] = None, *args, **kwargs
):
    # Code to acquire resource, e.g.:
    identifier = ""

    # We get the names of the arguments as sometimes they are not passed as kwargs and we need to identify
    # them in order to see if they are in the limit_to_keys.
    args_names = wrapped.__code__.co_varnames[: wrapped.__code__.co_argcount]

    for key, value in [*kwargs.items(), *list(zip(args_names, args))]:
        if not limit_to_keys or key in limit_to_keys:
            identifier += f"{key}:{value};"
    _hook_scope_manager.current_identifier.append(f"{id(wrapped)}{identifier}")
    try:
        yield
    finally:
        # Code to release resource, e.g.:
        _hook_scope_manager.current_identifier.pop()


_hook_scope_manager.current_identifier = []


def hook_scope(limit_to_keys: Optional[list[str]] = None) -> Callable:
    """
    Create a scope for all hooks in the scope. The scope will be added to the hook identifiers to allow for state to
    be scoped either per the function and below or by the function and keys.
    :param limit_to_keys: The keys to limit the scope to
    """

    # The function argument is called "__hooked_function" on purpose to be able to identify it in the frame utils
    def scope_decorator(__hooked_function__):
        @wraps(__hooked_function__)
        def wrapper(*args, **kwargs):
            with _hook_scope_manager(
                __hooked_function__, limit_to_keys, *args, **kwargs
            ):
                return __hooked_function__(*args, **kwargs)

        return wrapper

    return scope_decorator
