from functools import cached_property
from pathlib import Path

from sqlmodel import ARRAY, JSON, Column, Field, SQLModel, String

from src.hunting_target.python import PyTarget

__all__ = ["SQLTarget"]


class SQLTarget(SQLModel, table=True):  # type: ignore[call-arg]
    """A targetable, trackable object for comparison over time in storage."""

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
        return cls(**pytarget.dict())

    @cached_property
    def filename(self) -> Path:
        """File name for saving, omitting a suffix."""
        return Path(f"{self.name}_{self.creation_time}")
