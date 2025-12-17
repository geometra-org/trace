import tomllib
from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, ClassVar, Self

from src.settings.build_root import get_build_root
from src.type_mods.singleton import Singleton

ATTRS = ["project", "team", "version"]
INIT_KWARGS = {attr: None for attr in ATTRS}


class SupportedTomls(StrEnum):
    """All supported toml files."""

    PYHUNTERS = "pyhunters.toml"
    PYPROJECT = "pyproject.toml"

    @property
    def path(self) -> Path:
        """Convert string to path."""
        return Path(self.value)


@dataclass(frozen=True)
class TomlConfig(metaclass=Singleton):
    """Guide-ing params for setting up a Teaumehl object."""

    project: str | None
    team: str | None
    version: str | None

    @classmethod
    @abstractmethod
    def parse(cls, toml: dict[str, Any]) -> Self:
        """Parse a toml dictionary and extract fields."""


class PyHuntersToml(TomlConfig):
    """Guide-ing params for setting up a Teaumehl object."""

    project: str | None
    team: str | None
    version: str | None

    @classmethod
    def parse(cls, toml: dict[str, Any]) -> Self:
        """Parse, looking at top level keys."""
        return cls(
            project=toml.get("project"),
            team=toml.get("team"),
            version=toml.get("version"),
        )


class PyProjectToml(TomlConfig):
    """Guide-ing params for setting up a Teaumehl object."""

    project: str | None
    team: str | None
    version: str | None

    @classmethod
    def parse(cls, toml: dict[str, Any]) -> Self:
        """Parse, looking at both `project` key and `tool.pyhunters` key."""
        init_kwargs = INIT_KWARGS.copy()

        project_section = toml.get("project", {})
        pyhunters_section = toml.get("tool", {}).get("pyhunters", {})
        # pyhunters section will overwrite project section
        for key in ATTRS:
            init_kwargs[key] = (
                project_section.get(key)
                if project_section.get(key)
                else init_kwargs[key]
            )
            init_kwargs[key] = (
                pyhunters_section.get(key)
                if pyhunters_section.get(key)
                else init_kwargs[key]
            )

        return cls(**init_kwargs)


@dataclass(frozen=True)
class HuntingParty(metaclass=Singleton):
    """Conveniently create a Toml object."""

    @dataclass
    class Key:
        """Requirements to build a config."""

        filename: Path
        toml_config: type[TomlConfig]

    FILENAME_TOML_MAP: ClassVar[dict[SupportedTomls, Key]] = {
        SupportedTomls.PYHUNTERS: Key(
            filename=SupportedTomls.PYHUNTERS.path, toml_config=PyHuntersToml
        ),
        SupportedTomls.PYPROJECT: Key(
            filename=SupportedTomls.PYPROJECT.path, toml_config=PyProjectToml
        ),
    }

    project: str | None
    team: str | None
    version: str | None

    def __post_init__(self):
        """Ensure that no fields are `None`."""
        missing_fields = []
        for key, value in self.__dict__.items():
            if not value:
                missing_fields += [key]
        if missing_fields:
            raise ValueError(
                f"Could not parse required fields from toml files: {missing_fields}"
            )

    @classmethod
    def from_options(cls) -> Self:
        """Conveniently create a Toml object from a filename."""
        all_configs = []
        for toml_type in [SupportedTomls.PYPROJECT, SupportedTomls.PYHUNTERS]:
            toml_constructor = cls._identify_toml_type(toml_type)
            toml_obj = cls._conditionally_create(toml_constructor)
            if toml_obj:
                all_configs += [toml_obj]
        return cls.from_tomls(all_configs)

    @classmethod
    def from_tomls(cls, tomls: list[TomlConfig]) -> Self:
        """Create a RunConfig object from a list of toml files."""
        init_kwargs = INIT_KWARGS.copy()

        for toml in tomls:
            for attr in ATTRS:
                if init_kwarg := getattr(toml, attr):
                    init_kwargs[attr] = init_kwarg

        return cls(**init_kwargs)

    @classmethod
    def _identify_toml_type(cls, filename: SupportedTomls) -> Key:
        """Identify a toml class by filename."""
        try:
            return cls.FILENAME_TOML_MAP[filename]
        except KeyError as exc:
            raise ValueError(f"Unknown filename: {filename}") from exc

    @classmethod
    def _conditionally_create(cls, config_key: Key) -> TomlConfig | None:
        """Create a Toml object from a toml file."""
        root = get_build_root()
        full_path = root.path / config_key.filename
        try:
            with open(full_path, "rb") as toml:
                content = tomllib.load(toml)
        except FileNotFoundError:
            return None

        return config_key.toml_config.parse(content)


def rally_hunting_party():
    """Create a hunting party."""
    return HuntingParty.from_options()
