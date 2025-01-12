from dataclasses import dataclass
from trace import Trace


@dataclass
class Summarizer:
    _traces: set[Trace]
    result: dict[Trace, bool] | None = None

    def __post_init__(self):
        self.compare_all()

    def compare_all(self):
        """Compares all traces to their expectations, finally setting the `result` attr"""
        results = {}
        for trace in self._traces:
            results[trace] = trace.assert_expected
        self.result = results
