from dataclasses import dataclass
from collections.abc import Callable
import sys
import os


@dataclass
class Session:
    entrypoint: str
    func: str

    def __post_init__(self):
        self.exc_type: type[Exception] | None = None
        self.exc_value: str | None = None
        self.exc_tb: str | None = None

    @classmethod
    def from_call(cls, func: Callable):
        entrypoint = sys.argv[0].rsplit(os.path.sep, 1)[-1]
        return cls(entrypoint, func.__name__)

    def __enter__(self):
        yield

    def __exit__(self, exc_type: type[Exception], exc_value, exc_tb):
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_tb = exc_tb
