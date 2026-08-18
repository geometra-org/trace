from datetime import UTC, datetime
from functools import cached_property
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

from src.lumber import DEFAULT_INDENT, LOG_PREFIX

__all__ = ["PyTarget"]


class PyTarget(BaseModel):
    """A targetable, trackable object for comparison over time in storage."""

    # Hunting Party defaults
    project: str
    team: str
    version: str
    # Unique to target
    name: str
    module_path: Path
    method_name: str
    line_no: int
    args: tuple[object, ...]
    kwargs: dict[str, object]
    returns: object | None
    error: Exception | None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @cached_property
    def creation_time(self) -> datetime:
        """When a PyTarget was created."""
        return datetime.now(UTC)

    @model_validator(mode="after")
    def set_creation_time(self):
        """Set the creation time.

        Not much of a validator, just a way to set creation time
        """
        _ = self.creation_time
        return self

    @model_validator(mode="after")
    def check_returns_and_error(self) -> Self:
        """Ensure wonky initialization is caught."""
        if self.returns and self.error:
            raise ValueError(
                f"A {self.__class__.__name__} object cannot have both returns and an "
                "error."
            )
        return self

    def __eq__(self, other: object) -> bool:
        """Compare two `Target` objects for equality."""
        if not isinstance(other, type(self)):
            return False

        if self.error is None != other.error is None:
            return False

        errors_match = (
            type(self.error) is type(other.error) if self.error is not None else True
        )
        error_args_match = (
            getattr(self.error, "args", None) == getattr(other.error, "args", None)
            if self.error is not None
            else True
        )
        return (
            self.name == other.name
            and self.project == other.project
            and self.team == other.team
            and self.version == other.version
            and self.module_path == other.module_path
            and self.method_name == other.method_name
            and self.line_no == other.line_no
            and self.args == other.args
            and self.kwargs == other.kwargs
            and self.returns == other.returns
            and errors_match
            and error_args_match
        )

    @property
    def key(self) -> str:
        """Hashable of the `Target`-able object."""
        return (
            f"{self.project}.{self.name}:"
            f"{self.module_path}.{self.method_name}.{self.line_no}"
        )

    def __hash__(self) -> int:
        """One (unique) `Target` to rule them all."""
        return hash(self.key)

    def __str__(self) -> str:
        """`PyTarget` as a string."""
        return (
            f"{LOG_PREFIX}: PyTarget: {self.name}\n"
            f"{DEFAULT_INDENT}project     -> {self.project}\n"
            f"{DEFAULT_INDENT}team        -> {self.team}\n"
            f"{DEFAULT_INDENT}version     -> {self.version}\n"
            f"{DEFAULT_INDENT}module_path -> {self.module_path}\n"
            f"{DEFAULT_INDENT}method_name -> {self.method_name}\n"
            f"{DEFAULT_INDENT}line_no     -> {self.line_no}\n"
            f"{DEFAULT_INDENT}args        -> {self.args}\n"
            f"{DEFAULT_INDENT}kwargs      -> {self.kwargs}\n"
            f"{DEFAULT_INDENT}return      -> {self.returns}\n"
            f"{DEFAULT_INDENT}error       -> {self.error}\n"
        )

    @property
    def error_raised(self) -> bool:
        """Whether the `Target` caught an error."""
        return bool(self.error)
