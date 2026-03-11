"""Singletons are initialized only once."""

from typing import ClassVar


class Singleton(type):
    """Singleton, mingleton."""

    _instances: ClassVar[dict[type, object]] = {}

    def __call__(cls, *args, **kwargs):
        """Call me maybe."""
        key = (cls, *args, frozenset(kwargs.items()))
        if key not in cls._instances:
            cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]
