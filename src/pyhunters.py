import atexit
import inspect
import logging
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Self

from src.hunting_target.python import PyTarget
from src.lumber import LOG_PREFIX
from src.settings.config import HuntingParty, rally_hunting_party

__all__ = ["PyHunters"]
logger = logging.getLogger(__name__)


@dataclass
class PyHunters:
    """Class for adding and managing targets."""

    config: HuntingParty = field(default_factory=rally_hunting_party)
    targets: list[PyTarget] = field(default_factory=list)

    def __post_init__(self):
        """Ensure that the exit handler is registered."""
        self._register_exit()

    def __iter__(self):
        """Iterate through all the targets."""
        return iter(self.targets)

    def __getitem__(self, key: str) -> PyTarget:
        """Get a `Target` by name."""
        return self._map[key]

    def __len__(self) -> int:
        """Return the number of targets."""
        return len(self.targets)

    # cached properties identify an override or fallback to config default
    @cached_property
    def _project(self) -> str:
        """Get the project name."""
        return self.config.project

    @cached_property
    def _team(self) -> str:
        """Get the team name."""
        return self.config.team

    @cached_property
    def _version(self) -> str:
        """Get the version name.

        This is cannot be overwritten and is tied to the config.
        """
        return self.config.version

    def get(self, name: str, *, default: PyTarget | None = None) -> PyTarget | None:
        """Get a `PyTarget` by name, or default if not found."""
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
        return {target.name: target for target in self}

    def add(self, target: PyTarget) -> Self:
        """Add a target to the collection."""
        self.targets += [target]
        logger.info(f"{LOG_PREFIX}: Successfully marked target: {target}")
        return self

    def summarize(self):
        """Summarize all targets."""
        logger.info(f"{LOG_PREFIX}: Marked `{len(self)}` targets.")
        for driver in self.config.drivers:
            driver.save_many(self.targets)

    def mark(self, name: str):
        """Simple interface for marking a target."""
        caller = inspect.stack()[1]
        module_path = Path(caller.filename)

        # increment the line number by '1' to grab the correct line
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
                self.add(PyTarget(**mark_kwargs))
                return returns

            return wrapper

        return inner
