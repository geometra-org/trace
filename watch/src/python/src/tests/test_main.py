from main import main
import pytest

def test_factory(tmp):
    @main.watch(path = tmp)
    def fake_method():
        return "this"
