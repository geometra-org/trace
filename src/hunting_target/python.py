from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator

__all__ = ["PyTarget"]


class PyTarget(BaseModel):
    """A targetable, trackable object for comparison over time in storage."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    project: str
    team: str
    version: str
    module_path: Path
    method_name: str
    line_no: int
    args: tuple[object, ...]
    kwargs: dict[str, object]
    returns: object | None
    error: Exception | None

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
            self.project == other.project
            and self.name == other.name
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

    @property
    def error_raised(self) -> bool:
        """Whether the `Target` caught an error."""
        return bool(self.error)
