import atexit
import inspect
import os
import pathlib
from typing import TypeVar

# from .plan import Plan
from .summary import Summarizer
from .trace import Trace
from .type_mods.dictionary import swap_dict_key_values
from .type_mods.singleton import Singleton

T = TypeVar("T")


class Watcher(metaclass=Singleton):
    SCHEMA_SEP = "."
    _traces: set[Trace] = set()

    def __init__(self):
        self._register_exit()

    def _register_exit(self):
        """When the program exits, summarize the traces"""
        atexit.register(self.summarize)

    def add(self, value: T, expected: T | None):
        """Add a new variabe to track with optional expected comparision"""
        uid = self.make_unique_id(value)
        trace = Trace(uid, value, expected)
        self._traces.add(trace)

    def make_unique_id(self, value: object) -> str:
        """Generate a unique mapping key based on the "add"-ed value

        Args:
            value: any object to track

        Returns:
            str: hashable key for mapping
        """
        caller = inspect.stack()[2]  # Caller's frame is always two above

        pure_path = pathlib.PurePath(caller.filename)
        rel_path = pure_path.relative_to(os.getcwd())
        no_ext = rel_path.with_suffix("")
        components = str(no_ext).split(pathlib.os.sep)

        var_name = swap_dict_key_values(caller.frame.f_locals)[value]
        components += [var_name]

        return self.SCHEMA_SEP.join(components)

    def summarize(self):
        """Summarize all the traces"""
        return Summarizer(self._traces)


def getWatcher() -> Watcher:
    return Watcher()
