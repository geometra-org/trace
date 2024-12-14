from .singleton import Singleton
import inspect
from varname import nameof
import os


def getWatcher(name: str):
    return Watcher(name)


class Watcher(metaclass=Singleton):
    def __init__(self, name: str):
        self._queue = []

    def add(self, var: any):
        """Add a new variabe to track and optionally push its comparison to the queue"""
        uid = self.make_unique_id(var)
        pass

    def make_unique_id(self, var: any) -> str:
        breakpoint()
        path = inspect.stack()
        varname = nameof(var)
        return os.path.join(path, varnmae)
