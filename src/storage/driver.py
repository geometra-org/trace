import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Self

import pandas as pd
from sqlalchemy import Engine, create_engine
from sqlmodel import Session

from src.hunting_target.python import PyTarget
from src.hunting_target.sql import SQLTarget
from src.storage.config import LocalConfig, SQLAlchemyConfig

logger = logging.getLogger(__name__)
__all__ = ["Driver", "LocalDriver", "MultiDriver", "SQLAlchemyDriver"]


@dataclass
class Driver(ABC):
    """Abstract base class for saving targets to storage."""

    @classmethod
    @abstractmethod
    def from_config(cls, config) -> Self:
        """Create a driver from a config."""

    @abstractmethod
    def save(self, target: SQLTarget) -> None:
        """Save a target to the desired path."""

    @abstractmethod
    def save_many(self, targets: Iterable[PyTarget | SQLTarget]) -> None:
        """Save multiple targets to the desired path."""


@dataclass
class LocalDriver(Driver):
    """Local storage driver for saving SQL targets as csv files."""

    save_dir: Path

    @classmethod
    def from_config(cls, config: LocalConfig) -> Self:
        """Create a local DB driver from a config."""
        return cls(save_dir=config.save_dir)

    def save(self, target: PyTarget | SQLTarget) -> None:
        """Save a target locally as a csv.

        This is sort-of inefficient since we are duplicating read operations.
        """
        sql_target = (
            SQLTarget.from_pytarget(target) if isinstance(target, PyTarget) else target
        )
        self._check_save_dir()
        current_df = self._load_current(sql_target.filename)
        combined_df: pd.DataFrame = pd.concat([current_df, sql_target.as_df])
        combined_df.to_csv(self.save_path(sql_target.filename))

    def save_many(self, targets: Iterable[PyTarget | SQLTarget]) -> None:
        """Save multiple targets locally as csv.

        Unlique SQL storage, targets are separated between files to avoid massive
        tables and potentially inefficient lookups.
        """
        sql_targets: list[SQLTarget] = [
            SQLTarget.from_pytarget(target) if isinstance(target, PyTarget) else target
            for target in targets
        ]

        grouped_targets: dict[Path, list[SQLTarget]] = defaultdict(list)

        # Group targets by filename so that they can each be saved in one operation
        for target in sql_targets:
            grouped_targets[target.filename] += [target]

        # Save each group of targets to a single csv file
        for filename, target_list in grouped_targets.items():
            self._check_save_dir()
            current_df = self._load_current(filename)
            combined_df: pd.DataFrame = pd.concat(
                [current_df] + [target.as_df for target in target_list]
            )
            combined_df.to_csv(self.save_path(filename))

    def save_path(self, filename: Path) -> Path:
        """Full path to table."""
        return self.save_dir / Path(f"{filename}.csv")

    def _check_save_dir(self):
        """Check if the save directory exists, create if not."""
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True)

    def _load_current(self, filename: Path) -> pd.DataFrame:
        """Load the current version of the target."""
        try:
            return pd.read_csv(self.save_path(filename), index_col=SQLTarget.INDEX_COL)
        except FileNotFoundError:
            return pd.DataFrame()


@dataclass
class SQLAlchemyDriver(Driver):
    """Driver for saving targets to a SQL database via SQLAlchemy."""

    _engine: Engine

    @classmethod
    def from_config(cls, config: SQLAlchemyConfig) -> Self:
        """Create a SQLAlchemy driver from a config."""
        engine = create_engine(config.database_url)
        return cls(engine)

    def save(self, target: SQLTarget) -> None:
        """Save a target to a SQL database."""
        with Session(self._engine) as session:
            session.add(target)
            session.commit()

    def save_many(self, targets: Iterable[PyTarget | SQLTarget]) -> None:
        """Save multiple targets to a SQL database."""
        with Session(self._engine) as session:
            for target in targets:
                session.add(target)
            session.commit()


@dataclass
class MultiDriver:
    """Manager for saving files via engine(s)."""

    _drivers: list[Driver]

    @classmethod
    def create(cls, db_engine_configs: list[type[Driver]] | None) -> Self | None:
        """Create from engine names."""
        drivers: list[Driver] = []
        for config in db_engine_configs or []:
            drivers += [config.from_config(config)]

        return cls(drivers)

    def save(self, target: SQLTarget) -> None:
        """Save a single target to a destination."""
        for saver in self._drivers:
            saver.save(target)

    def save_many(self, targets: Iterable[PyTarget | SQLTarget]) -> None:
        """Save multiple targets to a destination."""
        for saver in self._drivers:
            saver.save_many(targets)
