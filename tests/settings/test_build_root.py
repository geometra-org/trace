from src.settings import build_root as module


class TestBuildRoot:
    """src.settings.build_root._BuildRoot."""

    test_cls = module.BuildRoot

    def test_path(self):
        """src.settings.build_root.BuildRoot.path."""
        test_obj = self.test_cls()
        assert test_obj.path.stem == "pyhunters"
