import logging
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from src.type_mods.singleton import Singleton

__all__ = ["get_build_root"]

# ordered in priority
root_files: list[str] = ["pyhunters.toml", "pyproject.toml"]
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _BuildRoot(metaclass=Singleton):
    """Represents the global workspace build root."""

    class NotFoundError(Exception):
        """Raised when unable to find the current workspace build root."""

    @cached_property
    def path(self) -> Path:
        """Returns the build root for the current workspace."""
        root = Path.cwd().resolve()
        while not any((root / file).is_file() for file in root_files):
            if root != root.parent:
                root = root.parent
            else:
                raise self.NotFoundError(
                    "No build root detected. `pyhunters` detects the build root by "
                    f"looking for at least one file from {root_files} in the cwd "
                    "and its ancestors."
                )
        logger.info(f"PYHUNTERS: Build root identified at `{root}`.")
        return root


def get_build_root() -> _BuildRoot:
    """Returns the build root for the current workspace.

    Defined separately for easy mocking.
    """
    return _BuildRoot()
