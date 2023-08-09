from typing import Callable, Optional

from contextlib import ContextDecorator
from functools import wraps
from uuid import uuid4

HOOK_SCOPE_ATTRIBUTE = "__hook_scope__"
HOOKED_FUNCTION_ATTRIBUTE = "__hooked_function__"


class __HookScopeDecorator(ContextDecorator):
    """
    For internal use.
    A decorator to create a scope for all hooks in the scope. The scope will be added to the hook identifiers to allow
    for state to be scoped either per the function and below or by the function and keys.
    """

    def __init__(self, wrapped: Callable, limit_to_keys: Optional[list[str]] = None):
        self._is_in_context = False
        self.wrapped = wrapped
        self.wrapped.__hook_scope__ = self
        self.limit_to_keys = limit_to_keys
        self.scope_identifier = str(uuid4())

    def __enter__(self):
        self._is_in_context = True
        return self

    def __exit__(self, *exc):
        self._is_in_context = False
        return False

    def identify(__hook_self, **kwargs) -> str:
        """
        Create an identifier for the hook. The identifier will be used to store the hook state in the store.
        We purposefully name the first argument __hook_self to avoid name collisions with the wrapped function.
        :param kwargs: The wrapped function arguments
        :return: The identifier
        """
        # We begin with the scope identifier to ensure functions without any arguments are still scoped.
        identifier = __hook_self.scope_identifier
        for key, value in kwargs.items():
            if not __hook_self.limit_to_keys or key in __hook_self.limit_to_keys:
                identifier += f"{key}:{value};"
        return identifier

    def in_context(self) -> bool:
        return self._is_in_context


def hook_scope(limit_to_keys: Optional[list[str]] = None) -> Callable:
    """
    Create a scope for all hooks in the scope. The scope will be added to the hook identifiers to allow for state to
    be scoped either per the function and below or by the function and keys.
    :param limit_to_keys: The keys to limit the scope to
    """

    # The function argument is called "__hooked_function" on purpose to be able to identify it in the frame utils
    def scope_decorator(__hooked_function__):
        @__HookScopeDecorator(__hooked_function__, limit_to_keys=limit_to_keys)
        @wraps(__hooked_function__)
        def wrapper(*args, **kwargs):
            return __hooked_function__(*args, **kwargs)

        return wrapper

    return scope_decorator
