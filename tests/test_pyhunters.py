from pathlib import Path

import pytest

from src import pyhunters as module
from src.target.python import PyTarget

TEST_TARGET = "test_target"

CONFIG_KWARGS = {
    "project": "TEST PROJECT",
    "team": "TEST TEAM",
    "version": "TEST VERSION",
}


@pytest.fixture
def test_pyhunters(mocker):
    """Fixture for forming a PyHunters instance."""
    return module.PyHunters(config=mocker.Mock(**CONFIG_KWARGS))


def test_mark_no_args_no_return(test_pyhunters: module.PyHunters):
    """src.pyhunters.PyHunters.mark.

    mark a method that uses no args and has no return
    """

    @test_pyhunters.mark(TEST_TARGET)
    def test_method_no_args_no_return():
        return

    test_method_no_args_no_return()
    actual_result = test_pyhunters[TEST_TARGET]
    expected_result = PyTarget(
        name=TEST_TARGET,
        **CONFIG_KWARGS,
        module_path=Path(__file__),
        method_name="test_method_no_args_no_return",
        line_no=30,
        args=(),
        kwargs={},
        returns=None,
        error=None,
    )
    assert actual_result == expected_result


def test_mark_no_args_w_return(test_pyhunters: module.PyHunters):
    """src.pyhunters.PyHunters.mark.

    mark a method that uses no args and has a return
    """

    @test_pyhunters.mark(TEST_TARGET)
    def test_mark_no_args_w_return():
        return "this", "that"

    test_mark_no_args_w_return()
    actual_result = test_pyhunters[TEST_TARGET]
    expected_result = PyTarget(
        name=TEST_TARGET,
        **CONFIG_KWARGS,
        module_path=Path(__file__),
        method_name="test_mark_no_args_w_return",
        line_no=56,
        args=(),
        kwargs={},
        returns=("this", "that"),
        error=None,
    )
    assert actual_result == expected_result


def test_mark_w_args_w_return(test_pyhunters: module.PyHunters):
    """src.pyhunters.PyHunters.mark.

    mark a method that uses args and has a return
    """
    TEST_TARGET = "test_target"

    @test_pyhunters.mark(TEST_TARGET)
    def test_method_w_args_w_return(number: int):
        mulitply_by = 3
        return number * mulitply_by

    test_method_w_args_w_return(5)
    actual_result = test_pyhunters[TEST_TARGET]
    expected_result = PyTarget(
        name=TEST_TARGET,
        **CONFIG_KWARGS,
        module_path=Path(__file__),
        method_name="test_method_w_args_w_return",
        line_no=83,
        args=(5,),
        kwargs={},
        returns=15,
        error=None,
    )
    assert actual_result == expected_result


def test_mark_w_kwargs_w_return(test_pyhunters: module.PyHunters):
    """src.pyhunters.PyHunters.mark.

    mark a method that uses kwargs and has a return
    """
    TEST_TARGET = "test_target"

    @test_pyhunters.mark(TEST_TARGET)
    def test_mark_w_kwargs_w_return(number: int):
        mulitply_by = 3
        return number * mulitply_by

    test_mark_w_kwargs_w_return(number=5)
    actual_result = test_pyhunters[TEST_TARGET]
    expected_result = PyTarget(
        name=TEST_TARGET,
        **CONFIG_KWARGS,
        module_path=Path(__file__),
        method_name="test_mark_w_kwargs_w_return",
        line_no=111,
        args=(),
        kwargs={"number": 5},
        returns=15,
        error=None,
    )
    assert actual_result == expected_result


def test_mark_no_args_w_raise(test_pyhunters: module.PyHunters):
    """src.pyhunters.PyHunters.mark.

    mark a method that uses no args and raises an error
    """

    @test_pyhunters.mark(TEST_TARGET)
    def test_mark_no_args_w_raise():
        raise ValueError

    try:
        test_mark_no_args_w_raise()
    except Exception:
        actual_result = test_pyhunters[TEST_TARGET]
        expected_result = PyTarget(
            name=TEST_TARGET,
            **CONFIG_KWARGS,
            module_path=Path(__file__),
            method_name="test_mark_no_args_w_raise",
            line_no=138,
            args=(),
            kwargs={},
            returns=None,
            error=ValueError(),
        )
        assert actual_result == expected_result
