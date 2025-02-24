from abc import abstractmethod
from enum import StrEnum, auto

from src.trace import Trace


class Dtypes(StrEnum):
    CSV = auto()
    JSON = auto()


class Saveable:
    """Ensures a common initial format regarldess of how the file is saved"""

    def __init__(self, content: dict[Trace, bool], dtype: str):
        self.content = content
        self.dtype = dtype

    @abstractmethod
    def save(self, path: str) -> None:
        """Save the content to a file at the given path"""
