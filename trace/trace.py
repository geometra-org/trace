from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass
class Trace:
    key: str
    value: T
    expected: T

    def __str__(self):
        return self.key

    def __hash__(self):
        return hash(self.key)

    def assert_expected(self) -> bool:
        """Compares the actual value to the expected

        Assumes that type `T` has a __eq__ method"""
        return self.value == self.expected

    def as_dict(self) -> dict[str, dict[str, T]]:
        return {str(self): {"actual": self.value, "expected": self.expected}}
