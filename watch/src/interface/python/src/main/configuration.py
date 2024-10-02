import tomllib
from dataclasses import dataclass
from .singleton import Singleton

GEOMETRA_TOML = "geometra.toml"

__all__ = ["Configuration"]


@dataclass
class Configuration(metaclass=Singleton):
    """Geometra setup and persistent settings"""

    relations: dict[str, str]

    @classmethod
    def from_toml(cls):
        """Loads in the configuration from `geometra.toml`"""
        with open(GEOMETRA_TOML, "rb") as f:
            raw_data = tomllib.load(f)
            return cls(**raw_data)
