from pydantic import Field

from src.hunting_target.core import Target

__all__ = ["PyTarget"]


class PyTarget(Target):
    """A targetable, trackable object for comparison over time in storage."""

    args: tuple[object, ...] = Field(exclude=True)
    kwargs: dict[str, object] = Field(exclude=True)
    returns: object | None = Field(exclude=True)
    error: Exception | None = Field(exclude=True)
