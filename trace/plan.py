from dataclasses import dataclass

from .type_mods.singleton import Singleton


@dataclass
class Plan(metaclass=Singleton):
    """TOML file based configuration"""

    save: bool

    @classmethod
    def from_toml(cls):
        pass
