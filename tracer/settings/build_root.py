# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import ClassVar

from pants.util.meta import SingletonMetaclass


@dataclass
class BuildRoot(metaclass=SingletonMetaclass):
    """Represents the global workspace build root."""

    root_files: ClassVar[list[str]] = ["trace.toml", "pyproject.toml"]

    class NotFoundError(Exception):
        """Raised when unable to find the current workspace build root."""

    @cached_property
    def path(self) -> Path:
        """Returns the build root for the current workspace."""
        root = Path.cwd().resolve()
        while not any((root / sentinel).is_file() for sentinel in self.root_files):
            if root != root.parent:
                root = root.parent
            else:
                raise self.NotFoundError(
                    "No build root detected. `trace` detects the build root by looking "
                    "for at least one file "
                    f"from {self.root_files} in the cwd and its ancestors."
                )
        return root
