from dataclasses import dataclass
from trace import Trace


@dataclass
class IOEntry:
    dtype: str


class Saveable:
    """Ensures a common initial format regarldess of how the file is saved"""

    def __init__(self, content: dict[Trace, bool]):
        self.content = content
