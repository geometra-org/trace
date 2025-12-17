from contextlib import AbstractContextManager, nullcontext
from pathlib import Path

import pytest

from src.hunting_target import python as module


class TestPyTarget:
    """src.hunting_target.python.PyTarget."""

    test_cls = module.PyTarget

    @pytest.mark.parametrize(
        "returns, error, context",
        [
            pytest.param(
                (123,),
                None,
                nullcontext(),
                id="valid-only-returns",
            ),
            pytest.param(
                None,
                None,
                nullcontext(),
                id="valid-no-returns-no-error",
            ),
            pytest.param(
                (123,),
                "ValueError()",
                pytest.raises(ValueError),
                id="invalid-both-returns-and-error",
            ),
        ],
    )
    def test_check_returns_and_error(
        self,
        returns: tuple,
        error: str,
        context: AbstractContextManager,
    ):
        """src.hunting_target.python.PyTarget.check_returns_and_error."""
        with context:
            _ = self.test_cls(
                name="test_target",
                project="Test Project",
                team="Test Team",
                version="1.0.0",
                module_path=Path(),
                method_name="test_method",
                line_no=1,
                args=(),
                kwargs={},
                returns=returns,
                error=error,
            )
