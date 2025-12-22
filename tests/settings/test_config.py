from pathlib import Path

import pytest

from src.settings import config as module

test_path = Path(__file__)


class TestPyHuntersToml:
    """src.settings.config.PyHuntersToml."""

    test_cls = module.PyHuntersToml

    def test_parse(self):
        """src.settings.config.PyHuntersToml.parse."""
        EXAMPLE_TOML = {
            "project": "TEST PROJECT",
            "team": "TEST TEAM",
            "version": "TEST VERSION",
            "save_result": True,
            "db_engines": ["TEST ENGINE"],
        }
        actual_result = self.test_cls.parse(EXAMPLE_TOML)
        expected_result = self.test_cls(
            project="TEST PROJECT",
            team="TEST TEAM",
            version="TEST VERSION",
            save_result=True,
            db_engines=["TEST ENGINE"],
        )
        assert actual_result == expected_result


class TestPyProjectToml:
    """src.settings.config.PyProjectToml."""

    test_cls = module.PyProjectToml

    def test_parse(self):
        """src.settings.config.PyProjectToml.parse."""
        EXAMPLE_TOML = {
            "tool": {
                "pyhunters": {
                    "project": "TEST PROJECT",
                    "team": "TEST TEAM",
                    "version": "TEST VERSION",
                    "save_result": True,
                    "db_engines": ["TEST ENGINE"],
                }
            }
        }
        actual_result = self.test_cls.parse(EXAMPLE_TOML)
        expected_result = self.test_cls(
            project="TEST PROJECT",
            team="TEST TEAM",
            version="TEST VERSION",
            save_result=True,
            db_engines=["TEST ENGINE"],
        )
        assert actual_result == expected_result


class TestHuntingParty:
    """src.settings.config.HuntingParty."""

    test_cls = module.HuntingParty

    @pytest.mark.parametrize(
        "pyproject_toml, pyhunters_toml, expected_result",
        [
            pytest.param(
                module.PyProjectToml(
                    project="OTHER PROJECT",
                    team="OTHER TEAM",
                    version="OTHER VERSION",
                    save_result=True,
                ),
                module.PyHuntersToml(
                    project="TEST PROJECT",
                    team="TEST TEAM",
                    version="TEST VERSION",
                    save_result=True,
                ),
                test_cls(
                    project="TEST PROJECT",
                    team="TEST TEAM",
                    version="TEST VERSION",
                    save_result=True,
                ),
                id="override-populated",
            ),
            pytest.param(
                module.PyProjectToml(
                    project=None,
                    team=None,
                    version=None,
                    save_result=True,
                ),
                module.PyHuntersToml(
                    project="TEST PROJECT",
                    team="TEST TEAM",
                    version="TEST VERSION",
                    save_result=True,
                ),
                test_cls(
                    project="TEST PROJECT",
                    team="TEST TEAM",
                    version="TEST VERSION",
                    save_result=True,
                ),
                id="override-none",
            ),
            pytest.param(
                module.PyProjectToml(
                    project=None,
                    team="OTHER TEAM",
                    version=None,
                    save_result=True,
                ),
                module.PyHuntersToml(
                    project="TEST PROJECT",
                    team=None,
                    version="TEST VERSION",
                    save_result=True,
                ),
                test_cls(
                    project="TEST PROJECT",
                    team="OTHER TEAM",
                    version="TEST VERSION",
                    save_result=True,
                ),
                id="mixed-override",
            ),
        ],
    )
    def test_from_tomls(
        self,
        pyproject_toml: module.PyProjectToml,
        pyhunters_toml: module.PyHuntersToml,
        expected_result: module.HuntingParty,
    ):
        """src.settings.config.HuntingParty.from_tomls."""
        actual_result = self.test_cls.from_tomls([pyproject_toml, pyhunters_toml])
        assert actual_result == expected_result
