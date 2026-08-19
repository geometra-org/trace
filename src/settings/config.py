import logging
import tomllib
from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, ClassVar, Self

from src.lumber import friendly_view
from src.settings.build_root import get_build_root
from src.storage.config import LocalConfig, SQLAlchemyConfig
from src.storage.driver import LocalDriver, SQLAlchemyDriver
from src.type_mods.singleton import SingletonMeta

logger = logging.getLogger(__name__)


class SupportedTomls(StrEnum):
    """All supported toml files."""

    PYHUNTERS = "pyhunters.toml"
    PYPROJECT = "pyproject.toml"

    @property
    def path(self) -> Path:
        """Convert string to path."""
        return Path(self.value)


@dataclass(frozen=True)
class ConfigParams:
    """All available fields in all toml file options."""

    project: str | None
    team: str | None
    version: str | None

    local_driver: LocalConfig | None = None
    sql_driver: SQLAlchemyConfig | None = None

    def __post_init__(self):
        """Warning message if no storage driver is set."""
        if self.local_driver is None and self.sql_driver is None:
            logger.warning("No storage driver set. Targets will NOT BE SAVED.")


class TomlConfig(ConfigParams, metaclass=SingletonMeta):
    """Guide-ing params for setting up a Teaumehl object."""

    filename: ClassVar[SupportedTomls]

    def __post_init__(self):
        """Log the created toml."""
        logger.info(str(self))

    def __str__(self) -> str:
        """Return a string representation of the toml config."""
        return friendly_view(self)

    @classmethod
    @abstractmethod
    def parse(cls, toml: dict[str, Any]) -> Self:
        """Parse a toml dictionary and extract fields."""


class PyHuntersToml(TomlConfig):
    """Guide-ing params for setting up a Teaumehl object."""

    filename: ClassVar[SupportedTomls] = SupportedTomls.PYHUNTERS

    @classmethod
    def parse(cls, toml: dict[str, Any]) -> Self:
        """Parse, looking at top level keys."""
        project = toml.get("project")
        team = toml.get("team")
        version = toml.get("version")
        local_driver = toml.get("local_driver")
        sql_driver = toml.get("sql_driver")

        return cls(
            project=project,
            team=team,
            version=version,
            local_driver=local_driver,
            sql_driver=sql_driver,
        )


class PyProjectToml(TomlConfig):
    """Guide-ing params for setting up a Teaumehl object."""

    filename: ClassVar[SupportedTomls] = SupportedTomls.PYPROJECT

    @classmethod
    def parse(cls, toml: dict[str, Any]) -> Self:
        """Parse, looking at both `project` key and `tool.pyhunters` key."""
        project_section = toml.get("project", {})
        pyhunters_section = toml.get("tool", {}).get("pyhunters", {})
        # pyhunters section will overwrite project section
        project = pyhunters_section.get("project") or project_section.get("name")
        team = pyhunters_section.get("team") or project_section.get("team")
        version = pyhunters_section.get("version") or project_section.get("version")
        local_driver = pyhunters_section.get("local_driver") or project_section.get(
            "local_driver"
        )
        sql_driver = pyhunters_section.get("sql_driver") or project_section.get(
            "sql_driver"
        )

        return cls(
            project=project,
            team=team,
            version=version,
            local_driver=local_driver,
            sql_driver=sql_driver,
        )


@dataclass(frozen=True)
class HuntingParty(metaclass=SingletonMeta):
    """Similar to `ConfigParams` but all fields are required."""

    project: str
    team: str
    version: str

    local_driver: LocalDriver | None = None
    sql_driver: SQLAlchemyDriver | None = None

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

    def __post_init__(self):
        """Log the final configuration."""
        logger.info(str(self))

    def __str__(self) -> str:
        """Return a string representation of the configuration."""
        return friendly_view(self)

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
        project = ""
        team = ""
        version = ""
        local_driver = None
        sql_driver = None

        for toml in tomls:
            if toml.project:
                project = toml.project
            if toml.team:
                team = toml.team
            if toml.version:
                version = toml.version
            if toml.local_driver:
                local_driver = toml.local_driver
            if toml.sql_driver:
                sql_driver = toml.sql_driver

        if not all([project, team, version]):
            missing = [
                attr
                for attr, value in [
                    ("project", project),
                    ("team", team),
                    ("version", version),
                ]
                if not value
            ]
            raise ValueError(f"Missing required fields for setup: {', '.join(missing)}")

        return cls(
            project=project,
            team=team,
            version=version,
            local_driver=LocalDriver.from_config(
                LocalConfig.model_validate(local_driver)
            )
            if local_driver
            else None,
            sql_driver=SQLAlchemyDriver.from_config(
                SQLAlchemyConfig.model_validate(sql_driver)
            )
            if sql_driver
            else None,
        )

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

    @property
    def drivers(self):
        """Return the local and SQLAlchemy drivers."""
        drivers = []
        if self.local_driver is not None:
            drivers += [self.local_driver]
        if self.sql_driver is not None:
            drivers += [self.sql_driver]
        return drivers


def rally_hunting_party() -> HuntingParty:
    """Create a hunting party."""
    return HuntingParty.from_options()
