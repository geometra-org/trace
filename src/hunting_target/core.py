from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Target(BaseModel):
    """A targetable, trackable object for comparison over time."""

    # Hunting Party defaults
    project: str
    team: str
    version: str

    # Target details
    name: str
    module_path: Path
    method_name: str
    line_no: int

    # varies based on child class
    args: tuple[object, ...] | tuple[bytes, ...] = Field(exclude=True)
    kwargs: dict[str, object] | dict[str, bytes] = Field(exclude=True)
    returns: object | bytes | None = Field(exclude=True)
    error: Exception | bytes | None = Field(exclude=True)

    # Default is intended
    creation_time: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)

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

    @cached_property
    def filename(self) -> Path:
        """File name for saving, omitting a suffix."""
        return Path(f"{self.project}_{self.team}_{self.version}")

    @property
    def error_raised(self) -> bool:
        """Whether the `Target` caught an error."""
        return bool(self.error)
