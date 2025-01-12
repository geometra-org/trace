from dataclasses import dataclass
from .type_mods.singleton import Singleton
from enum import StrEnum


class Dtypes(StrEnum):
    CSV = auto()
    JSON = auto()


@dataclass
class Plan(metaclass=Singleton):
    """TOML file based configuration"""

    save: bool

    @classmethod
    def from_toml(cls):
        pass
