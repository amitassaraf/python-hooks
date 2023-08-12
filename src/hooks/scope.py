# mypy: ignore-errors

from typing import Any, Callable, Optional

from contextlib import contextmanager
from functools import wraps

HOOKED_FUNCTION_ATTRIBUTE = "__hooked_function__"


@contextmanager
def _hook_scope_manager(
    wrapped: Callable[[Any], Any],
    limit_to_keys: Optional[list[str]] = None,
    *args: Any,
    **kwargs: dict[str, Any],
) -> None:
    """
    A context manager to manage the scope of hooks. This is used to identify the scope of hooks and to limit the scope
    of hooks to the function and keys.
    :param wrapped: The function that is being wrapped
    :param limit_to_keys: The keys to limit the scope to
    :param args: The args of the function
    :param kwargs: The kwargs of the function
    """

    # Code to acquire resource, e.g.:
    identifier = ""

    # We get the names of the arguments as sometimes they are not passed as kwargs and we need to identify
    # them in order to see if they are in the limit_to_keys.
    args_names = wrapped.__code__.co_varnames[: wrapped.__code__.co_argcount]

    for key, value in [*kwargs.items(), *list(zip(args_names, args))]:
        if limit_to_keys is None or key in limit_to_keys:
            identifier += f"{key}:{value};"
    _hook_scope_manager.current_identifier.append(f"{wrapped.__qualname__}{identifier}")
    try:
        yield
    finally:
        # Code to release resource, e.g.:
        _hook_scope_manager.current_identifier.pop()


_hook_scope_manager.current_identifier = []


def hook_scope(
    limit_to_keys: Optional[list[str]] = None, use_global_scope: Optional[bool] = False
) -> Callable[[Any], Any]:
    """
    Create a scope for all hooks in the scope. The scope will be added to the hook identifiers to allow for state to
    be scoped either per the function and below or by the function and keys.
    :param limit_to_keys: The keys to limit the scope to.
    :param use_global_scope: If True, the scope and all hooks will be persisted globally and will not be limited to the
     instance. If this is True, you must specify the keys to limit the scope to because we cannot identify the self / cls
        argument automatically.
    """

    if use_global_scope and limit_to_keys is None:
        raise ValueError(
            "You must specify the keys to limit the state to (limit_to_keys) if you want to use global "
            "scope, if your function only has self or cls as arguments, you can use an empty list '[]'."
        )

    # The function argument is called "__hooked_function" on purpose to be able to identify it in the frame utils
    def scope_decorator(__hooked_function__) -> Callable[[Any], Any]:
        __hooked_function__.use_global_scope = use_global_scope

        @wraps(__hooked_function__)
        def wrapper(*args, **kwargs) -> Any:
            with _hook_scope_manager(
                __hooked_function__, limit_to_keys, *args, **kwargs
            ):
                return __hooked_function__(*args, **kwargs)

        return wrapper

    return scope_decorator
