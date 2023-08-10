# type: ignore[attr-defined]
"""A React inspired way to code in Python"""

from importlib import metadata as importlib_metadata


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()

from .reducers import *
from .scope import *
from .use import *
