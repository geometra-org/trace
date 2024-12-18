from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


def swap_dict_key_values(dictionary: dict[K, V]) -> dict[V, K]:
    """Dictionary keys becomes values and values become keys"""
    return dict((v, k) for k, v in dictionary.items())
