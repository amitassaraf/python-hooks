# mypy: ignore-errors

from __future__ import annotations

from types import FrameType, FunctionType, MethodType
from typing import Any, Callable

import sys

from pyhashxx import hashxx

from .backends.backend_state import get_hooks_backend
from .backends.interface import HooksBackend
from .backends.python_objects_backend import python_object_backend_factory
from .scope import HOOKED_FUNCTION_ATTRIBUTE, _hook_scope_manager

SPECIAL_HOOKS = ["create_context"]


def __identify_function_and_owner(
    frame: FrameType | None | Any,
) -> tuple[Callable[[Any], Any] | None, Any]:
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
        if frame:
            for arg, arg_value in frame.f_locals.items():
                if arg == HOOKED_FUNCTION_ATTRIBUTE:
                    return arg_value, None

    if frame:
        return at.get(frame.f_code.co_name, None), value
    return None, value


def __frame_parts_to_identifier(*args: Any) -> str:
    """
    Get a unique identifier for the frame. This is used to identify the hook that called the current function frame.
    :return: A unique identifier for the frame
    """
    return "".join(map(str, args))


# type: ignore
def __identify_hook_and_backend(
    always_global_backend: bool = False,
    prefix: str = "",
) -> tuple[str, type[HooksBackend] | HooksBackend]:
    """
    Identify the hook that called the current function frame and the backend that should be used to backend the hook's
    state. If the hook is called from a method, the backend is a PythonObjectBackend. If the hook is called from a static
    method, the backend is a PickleBackend. If the hook is called from a function, the backend is a PickleBackend.
    :param always_global_backend: If True, the backend will always be a PickleBackend regardless of the hook's caller
    :param prefix: A prefix to add to the hook identifier
    :return: The hook identifier and the backend that should be used to backend the hook's state
    """
    # The use of _getframe is not ideal, but it is more performant than using inspect.currentframe
    frame: FrameType | None | Any = sys._getframe()
    if not frame:
        raise RuntimeError(
            "Could not identify the hook that called the current function"
        )

    frame: FrameType | None | Any = frame.f_back.f_back

    if not frame:
        raise RuntimeError(
            "Could not identify the hook that called the current function"
        )

    identifier_prefix = ""

    # Skip all hook functions in order to identify the function that called the hook
    while (
        frame.f_code.co_name.startswith("use_")
        or frame.f_globals["__name__"].startswith("hooks.")
    ) and frame.f_code.co_name not in SPECIAL_HOOKS:
        # We add a prefix to the identifier to ensure that the identifier is unique and that we can use hooks inside
        # hooks
        identifier_prefix += __frame_parts_to_identifier(
            frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name
        )
        frame = frame.f_back

    frame_identifier = identifier_prefix + __frame_parts_to_identifier(
        frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name
    )

    # We identify the function that called the hook and its owner
    caller_function, owner = __identify_function_and_owner(frame)

    # We identify the type of the function that called the hook
    is_static_method = isinstance(caller_function, staticmethod)
    is_class_method = isinstance(caller_function, classmethod)
    is_method = owner is not None and not is_static_method and not is_class_method
    is_scoped_globally = hasattr(caller_function, "use_global_scope") and getattr(
        caller_function, "use_global_scope", False
    )
    always_global_backend = always_global_backend or is_scoped_globally

    # In case the owner we found is a class, we try to find the instance of the class in the frame locals (self)
    if (is_method or is_class_method) and getattr(owner, "__class__", None) == type:
        for _, value in frame.f_locals.items():
            if isinstance(value, owner):
                owner = value
                break

    # Always add the current hook scope identifier to the frame identifier
    frame_identifier += ";".join(_hook_scope_manager.current_identifier)

    # If the hook is called from a method, we use a PythonObjectBackend to backend the hook's state.
    if (not is_method and not is_class_method) or always_global_backend:
        _backend = get_hooks_backend()
        return (
            str(hashxx(f"{prefix}{frame_identifier}".encode())),
            _backend,
        )

    return (
        str(hashxx(f"{prefix}{frame_identifier}{frame.f_code.co_name}".encode())),
        python_object_backend_factory(owner),
    )
