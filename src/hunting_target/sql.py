import uuid
from datetime import datetime
from functools import cached_property
from pathlib import Path

import pandas as pd
from sqlmodel import ARRAY, JSON, Column, Field, SQLModel, String

from src.hunting_target.python import PyTarget

__all__ = ["SQLTarget"]


class SQLTarget(SQLModel, table=True):  # type: ignore[call-arg]
    """A targetable, trackable object for comparison over time in storage."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    project: str
    team: str
    version: str
    module_path: Path
    method_name: str
    line_no: int
    creation_time: datetime
    args: tuple[bytes, ...] = Field(sa_column=Column(ARRAY(String)))
    kwargs: dict[str, bytes] = Field(sa_column=Column(JSON))
    returns: bytes | None
    error: bytes | None

    @classmethod
    def from_pytarget(cls, pytarget: PyTarget):
        """Convert a PyTarget pydantic model to a SQL model."""
        return cls(**pytarget.model_dump())

    @cached_property
    def filename(self) -> Path:
        """File name for saving, omitting a suffix."""
        return Path(f"{self.project}_{self.team}_{self.version}")

    @cached_property
    def as_df(self) -> pd.DataFrame:
        """Return a pandas DataFrame representation of this target."""
        return pd.DataFrame([self.model_dump()])
