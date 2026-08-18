import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

__all__ = ["LocalConfig", "SQLAlchemyConfig"]


@dataclass
class LocalConfig:
    """Configuration for the local storage driver."""

    save_dir: Path


@dataclass
class SQLAlchemyConfig:
    """Configuration for the SQL storage driver."""

    database_url: str
