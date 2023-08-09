from __future__ import annotations

from types import FrameType, FunctionType, MethodType
from typing import Any, Callable

import sys

from .scope import HOOK_SCOPE_ATTRIBUTE, HOOKED_FUNCTION_ATTRIBUTE
from .store import Store, _get_current_store, python_object_store_factory

SPECIAL_HOOKS = ["create_context"]


def __identify_function_and_owner(frame: FrameType) -> tuple[Callable | None, Any]:
    """
    Find the owner of the function that called the current function frame. If the function is a method, the owner is
    the class of the instance. If the function is a static method, the owner is the class of the static method.
    :param frame: The frame of the function that called the current function
    :return: The function instance and the owner of the function that called the current function frame
    """
    at: dict[str, Any] = {**frame.f_globals, **frame.f_locals}
    value: Any = None
    if hasattr(frame.f_code, "co_qualname"):
        for part in frame.f_code.co_qualname.split(".")[:-1]:
            for name, value in at.items():
                if name == part:
                    at = value.__dict__
                    break
    else:
        caller_name = frame.f_code.co_name
        # In the case we cannot find the owner using the qualname which is safest, we try to find the owner using the
        # function args. This is not safe because the function args can be anything, but it is better than nothing.
        for arg, arg_value in frame.f_locals.items():
            if hasattr(arg_value, caller_name) and isinstance(
                getattr(arg_value, caller_name), (FunctionType, MethodType)
            ):
                return getattr(arg_value, caller_name), arg_value

        # Finally, we will try to find a hooked function in the frame stack which is provided by the hook decorator to
        # help us limit the scope of hooks for global functions without owners.
        frame = frame.f_back
        for arg, arg_value in frame.f_locals.items():
            if arg == HOOKED_FUNCTION_ATTRIBUTE:
                return arg_value, None

    return at.get(frame.f_code.co_name, None), value


def __frame_parts_to_identifier(*args) -> str:
    """
    Get a unique identifier for the frame. This is used to identify the hook that called the current function frame.
    :return: A unique identifier for the frame
    """
    return "".join(map(str, args))


def __identify_hook_and_store(
    always_global_store: bool = False,
) -> tuple[str, type[Store] | Store]:
    """
    Identify the hook that called the current function frame and the store that should be used to store the hook's
    state. If the hook is called from a method, the store is a PythonObjectStore. If the hook is called from a static
    method, the store is a PickleStore. If the hook is called from a function, the store is a PickleStore.
    :param always_global_store: If True, the store will always be a PickleStore regardless of the hook's caller
    :return: The hook identifier and the store that should be used to store the hook's state
    """
    # The use of _getframe is not ideal, but it is more performant than using inspect.currentframe
    frame = sys._getframe().f_back.f_back
    identifier_prefix = ""

    # Skip all hook functions in order to identify the function that called the hook
    while (
        frame.f_code.co_name.startswith("use_")
        and frame.f_code.co_name not in SPECIAL_HOOKS
    ):
        # We add a prefix to the identifier to ensure that the identifier is unique and that we can use hooks inside
        # hooks
        identifier_prefix += __frame_parts_to_identifier(
            frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name
        )
        frame = frame.f_back

    frame_identifier = identifier_prefix + __frame_parts_to_identifier(
        frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name
    )

    caller_function, owner = __identify_function_and_owner(frame)
    is_static_method = isinstance(caller_function, staticmethod)
    is_class_method = isinstance(caller_function, classmethod)
    is_method = owner is not None and not is_static_method and not is_class_method

    if (is_method or is_class_method) and getattr(owner, "__class__", None) == type:
        for _, value in frame.f_locals.items():
            if isinstance(value, owner):
                owner = value
                break

    if (
        caller_function
        and getattr(caller_function, HOOK_SCOPE_ATTRIBUTE, None) is not None
    ):
        scope = getattr(caller_function, HOOK_SCOPE_ATTRIBUTE)
        if scope.in_context():
            frame_identifier += scope.identify(**frame.f_locals)

    # If the hook is called from a method, we use a PythonObjectStore to store the hook's state.
    if (not is_method and not is_class_method) or always_global_store:
        _store = _get_current_store()
        return (
            frame_identifier,
            _store,
        )

    return (
        f"{frame_identifier}{frame.f_code.co_name}",
        python_object_store_factory(owner),
    )
