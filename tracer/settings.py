from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    """Class for default global values."""

    project: str

    @classmethod
    def ingest_toml(self):
        """Defaults from `pyproject.toml`."""
        Path(__file__)
