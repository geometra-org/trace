from dataclasses import dataclass
import pandas as pd


@dataclass
class Exportinator:
    path: str

    @classmethod
    def from_session(cls, path: str):
        return cls(path)

    def export(self, table: pd.DataFrame) -> bool:
        try:
            table.to_csv(self.path)
        except Exception as _:
            return False
        return True
