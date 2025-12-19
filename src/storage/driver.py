import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from src.lumber import LOG_PREFIX
from src.settings.build_root import get_build_root
from src.target.sql import SQLTarget

logger = logging.getLogger(__name__)
__all__ = ["SQLDriver"]


@dataclass
class Engine(ABC):
    _connection: SQLConnection | None
    path: str

    @abstractmethod
    def save(self, target: SQLTarget) -> None:
        """Save a target to the desired path."""


@dataclass
class Local(Engine):
    _connection: None = None
    path: Path = get_build_root().path

    def save(self, target: SQLTarget) -> None:
        """Save a target locally as a csv."""
        with open(self.path + target.project + ".csv") as file:
            file.append(self.target)


@dataclass
class SQLDriver:
    """Manager for saving files via engine."""

    engines: list[Engine] | None = Local
    default_destination: Path = get_build_root().path

    @classmethod
    def create(cls, connection_string: str):
        """Create from a connection string."""

    def compute_destination(self, engine: Engine, destination: str | None) -> str:
        """Helper to use a default destination."""
        return engine.destination or self.default_destination

    def save(self, target: SQLTarget, destination: str | None = None) -> None:
        """Save a single target to a destination."""
        destination = self.compute_destination(destination)
        self._connection.save(target, destination)

    def save_many(self, targets: Iterable[SQLTarget], destination) -> None:
        """Save multiple targets to a destination."""
        # The nesting here is ugly but it's seemingly inevitable
        for engine in self.engines:
            for target in targets:
                try:
                    engine.save(target)
                except Exception:
                    logger.error(
                        f"{LOG_PREFIX}: Failed to save target `{target.name}` to"
                        " destination `{destination}`"
                    )
