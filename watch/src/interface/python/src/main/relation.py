from dataclasses import dataclass
import pandas as pd
from .session import Session


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

    @classmethod
    def from_session(cls, session: Session):
        return cls("this", "that", "abc")
