import pytest
from src.type_mods import dictionary as module


@pytest.mark.parametrize(
    "input_dict, expected_output",
    [
        pytest.param({1: "a", 2: "b"}, {"a": 1, "b": 2}, id="swap_dict_key_values_1"),
        pytest.param({"a": 1, "b": 2}, {1: "a", 2: "b"}, id="swap_dict_key_values_2"),
    ],
)
def test_swap_dict_key_values(input_dict: dict, expected_output: dict):
    """type_mods.swap_dict_key_values."""
    actual_output = module.swap_dict_key_values(input_dict)
    assert actual_output == expected_output
