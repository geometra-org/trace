"""Singletons are initialized only once."""

from typing import ClassVar


class SingletonMeta(type):
    """Singleton, mingleton."""

    _instances: ClassVar = {}

    def __call__(cls, *args, **kwargs):
        """Call me always, instantiate me maybe."""
        if cls not in cls._instances:
            # Call the parent class constructor and store the instance
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
