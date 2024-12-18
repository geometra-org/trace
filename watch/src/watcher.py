from .singleton import Singleton
from dataclasses import dataclass
from .type_mods.dictionary import swap_dict_key_values
import atexit
import pathlib
import asyncio
import inspect
import os


def getWatcher():
    return Watcher()


@dataclass
class Traceable:
    key: str
    value: object

class Watcher(metaclass=Singleton):
    SCHEMA_SEP = "."
    _queue: list[Traceable] = []
    _traces: set[Traceable] = set()

    def __init__(self):
        self._register_exit()
        
    def _register_exit(self):
        atexit.register(self.summarize)

    def add(self, value: object):
        """Add a new variabe to track and optionally push its comparison to the queue"""
        uid = self.make_unique_id(value)
        trace = Traceable(uid, value)
        pass

    def add_trace(self, trace: Traceable) -> None:
        self._queue += [trace]
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

    async def

    def summarize(self):
        pass
    
@dataclass
class Queue: