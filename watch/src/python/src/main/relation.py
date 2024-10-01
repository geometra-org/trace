from dataclasses import dataclass
import pandas as pd


@dataclass
class GitMetadata:
    tag: str
    branch: str
    execution_time: pd.Timestamp


@dataclass
class Relation:
    exception: str
    traceback: str
    git_metadata: GitMetadata

    def as_rustlike(self):
        """Transform the relation into a rust compatible type"""
        pass
