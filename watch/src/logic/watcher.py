from .type_mods.singleton import Singleton
from .trace import Trace

# from .plan import Plan
from .summary import Summarizer
import atexit
import pathlib
from .type_mods.dictionary import swap_dict_key_values
import inspect
from typing import TypeVar
import os

T = TypeVar("T")


def getWatcher() -> Watcher:
    return Watcher()


class Watcher(metaclass=Singleton):
    SCHEMA_SEP = "."
    _traces: set[Trace] = set()

    def __init__(self):
        self._register_exit()

    def _register_exit(self):
        atexit.register(self.summarize)

    def add(self, value: T, expected: T | None):
        """Add a new variabe to track with optional expected comparision"""
        uid = self.make_unique_id(value)
        trace = Trace(uid, value, expected)
        self._traces.add(trace)

    def make_unique_id(self, value: object) -> str:
        """Generate a unique mapping key based on the "add"-ed value

        Args:

        Returns:
            str: hashable key for mapping
        """
        caller = inspect.stack()[2]

        pure_path = pathlib.PurePath(caller.filename)
        rel_path = pure_path.relative_to(os.getcwd())
        no_ext = rel_path.with_suffix("")
        components = str(no_ext).split(pathlib.os.sep)

        var_name = swap_dict_key_values(caller.frame.f_locals)[value]
        components += [var_name]

        return self.SCHEMA_SEP.join(components)

    def summarize(self):
        summary = Summarizer(self._traces)
        breakpoint()
