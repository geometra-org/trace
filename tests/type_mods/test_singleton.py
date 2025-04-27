from dataclasses import dataclass

from src.type_mods import singleton as module


@dataclass
class SampleClass(metaclass=module.Singleton):
    name: str


class TestSingleton:
    def test_one_instance(self):
        obj_1 = SampleClass("one")
        obj_2 = SampleClass("two")
        assert obj_1 == obj_2
