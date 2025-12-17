import atexit
import inspect
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Self

from src.hunting_target.python import PyTarget
from src.settings.config import HuntingParty, rally_hunting_party

__all__ = ["PyHunters"]


@dataclass
class PyHunters:
    """Class for adding and managing marks."""

    config: HuntingParty | None = None
    team: str | None = None
    project: str | None = None
    version: str | None = None

    def __post_init__(self):
        """Ensure that the exit handler is registered."""
        self.config = self.config or rally_hunting_party()
        self.targets = []
        self._register_exit()

    def __iter__(self):
        """Iterate through all the marks."""
        return iter(self.targets)

    def __getitem__(self, key: str) -> PyTarget:
        """Get a `Target` by name."""
        return self._map[key]

    @cached_property
    def _project(self):
        """Get the project name."""
        return self.project or self.config.project

    @cached_property
    def _team(self):
        """Get the team name."""
        return self.team or self.config.team

    @cached_property
    def _version(self):
        """Get the version name."""
        return self.version or self.config.version

    def get(self, name: str, *, default: PyTarget | None = None) -> PyTarget | None:
        """Get a `Target` by name, or None if not found."""
        try:
            return self._map[name]
        except KeyError:
            return default

    def _register_exit(self):
        """Register the exit handler to summarize all targets."""
        atexit.register(self.summarize)

    @property
    def _map(self):
        """Get a dictionary mapping target names to targets."""
        return {target.name: target for target in self.targets}

    def add(self, target: PyTarget) -> Self:
        """Add a target to the collection."""
        if not isinstance(target, PyTarget):
            raise TypeError(f"Expected Target, got {type(target)}.")
        self.targets += [target]
        return self

    def summarize(self):
        """Summarize all targets."""
        pass

    def mark(self, name: str):
        """Simple interface for adding a marker."""
        caller = inspect.stack()[1]
        module_path = Path(caller.filename)
        line_no = caller.lineno + 1
        mark_kwargs = {
            "name": name,
            "project": self._project,
            "team": self._team,
            "version": self._version,
            "module_path": module_path,
            "line_no": line_no,
        }

        def inner(func):
            method_name = func.__name__
            mark_kwargs["method_name"] = method_name

            def wrapper(*args, **kwargs):
                """Inner actions within the method."""
                mark_kwargs["args"] = args
                mark_kwargs["kwargs"] = kwargs
                try:
                    returns = func(*args, **kwargs)
                except Exception as exc:
                    mark_kwargs["error"] = exc
                    mark_kwargs["returns"] = None
                    self.add(PyTarget(**mark_kwargs))
                    raise exc
                mark_kwargs["error"] = None
                mark_kwargs["returns"] = returns
                target = PyTarget.model_validate(mark_kwargs)
                self.add(target)
                return returns

            return wrapper

        return inner
