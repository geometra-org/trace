import pickle
import uuid
from functools import cached_property

import pandas as pd
from sqlmodel import ARRAY, JSON, Column, Field, SQLModel, String

from src.hunting_target.core import Target
from src.hunting_target.python import PyTarget

__all__ = ["SQLTarget"]


class SQLTarget(SQLModel, Target, table=True):  # type: ignore[call-arg]
    """A targetable, trackable object for comparison over time in storage."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    args: tuple[bytes, ...] = Field(sa_column=Column(ARRAY(String)))
    kwargs: dict[str, bytes] = Field(sa_column=Column(JSON))
    returns: bytes | None
    error: bytes | None

    @classmethod
    def from_pytarget(cls, pytarget: PyTarget):
        """Convert a PyTarget pydantic model to a SQL model."""
        args = pickle.dumps(pytarget.args) if pytarget.args else None
        kwargs = pickle.dumps(pytarget.kwargs) if pytarget.kwargs else None
        returns = pickle.dumps(pytarget.returns) if pytarget.returns else None
        error = pickle.dumps(pytarget.error) if pytarget.error else None
        return cls(
            **pytarget.model_dump(),
            args=args,
            kwargs=kwargs,
            returns=returns,
            error=error,
        )

    @cached_property
    def as_df(self) -> pd.DataFrame:
        """Return a pandas DataFrame representation of this target."""
        return pd.DataFrame([self.model_dump()])
