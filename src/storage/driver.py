import logging
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import pandas as pd
from sqlmodel import Engine, Session, SQLModel

from src.hunting_target.sql import SQLTarget
from src.settings.build_root import get_build_root

logger = logging.getLogger(__name__)
__all__ = ["SQLDriver"]


@dataclass
class Saver(ABC):
    @abstractmethod
    def save(self, target: SQLTarget) -> None:
        """Save a target to the desired path."""

    @abstractmethod
    def save_many(self, targets: list[SQLTarget]) -> None:
        """Save multiple targets to the desired path."""


@dataclass
class Local(Saver):
    _path: Path | None

    def __post_init__(self):
        """Use the build root path if no path is provided."""
        if self._path is None:
            self._path = get_build_root().path

    def save(self, target: SQLTarget) -> None:
        """Save a target locally as a csv.

        This is sort-of inefficient since we are duplicating read operations.
        """
        self._check_path(target)
        current_df = self._load_current(target)
        df = pd.DataFrame.from_records(target.to_dict())
        combined_df = pd.concat([current_df, df])
        sorted_df = combined_df.sort_values(by="creation_time", inplace=True)
        sorted_df.to_csv(self.save_dir(target) / f"{target.filename}.csv")

    def save_many(self, targets: list[SQLTarget]) -> None:
        """Save multiple targets locally as csv."""
        for target in targets:
            self.save(target)

    def save_dir(self, target: SQLTarget) -> Path:
        """Full path to table."""
        return self._path / target.filename

    def _check_path(self, target: SQLTarget):
        """Check if the path exists, creating if not."""
        if not self.save_dir(target).exists():
            self._path.mkdir(parents=True)

    def _load_current(self, target: SQLTarget) -> pd.DataFrame:
        """Load the current version of the target."""
        return pd.read_csv(self.save_dir / f"{self.target.filename}.csv")


@dataclass
class SQLAlchemy(Saver):
    _engine: Engine

    def save(self, target: SQLTarget) -> None:
        """Save a target to a SQL database."""
        with Session(self._engine) as session:
            session.add(target)
            session.commit()

    def save_many(self, targets: list[SQLTarget]) -> None:
        """Save multiple targets to a SQL database."""
        with Session(self._engine) as session:
            for target in targets:
                session.add(target)
            session.commit()


@dataclass
class SQLDriver:
    """Manager for saving files via engine(s)."""

    engines: list[Engine]

    def __post_init__(self):
        """Finalize SQL model metadata."""
        SQLModel.metadata.create_all(self.engines)

    @classmethod
    def create(
        cls, db_engines: list[str] | None, local_save_dir: Path | None = None
    ) -> Self | None:
        """Create from engine names."""
        if not db_engines:
            return None
        engines = []
        if "local" in db_engines:
            engines += [Local(local_save_dir)]
            db_engines.remove("local")
        engines += db_engines

        return cls(engines)

    def compute(self, engine: Engine, destination: Path | None) -> Path:
        """Helper to use a default destination."""
        return engine.destination or self.local_save_dir

    def save(self, target: SQLTarget) -> None:
        """Save a single target to a destination."""
        for engine in self.engines:
            engine.save(target)

    def save_many(self, targets: Iterable[SQLTarget], destination) -> None:
        """Save multiple targets to a destination."""
        for engine in self.engines:
            engine.save_many(targets)
