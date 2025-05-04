from dataclasses import dataclass

from src.type_mods import singleton as module


@dataclass
class SampleClass(metaclass=module.Singleton):
    """placeholder."""

    name: str


class TestSingleton:
    """type_mods.singleton.Singleton."""

    def test_one_instance(self):
        """type_mods.singleton.Singleton."""
        obj_1 = SampleClass("one")
        obj_2 = SampleClass("two")
        assert obj_1 == obj_2
