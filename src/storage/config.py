import logging
from pathlib import Path

from pydantic import BaseModel

logger = logging.getLogger(__name__)

__all__ = ["LocalConfig", "SQLAlchemyConfig"]


class LocalConfig(BaseModel):
    """Configuration for the local storage driver."""

    save_dir: Path


class SQLAlchemyConfig(BaseModel):
    """Configuration for the SQL storage driver."""

    database_url: str
