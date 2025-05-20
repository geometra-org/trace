from tracer import mark


@mark()
def example(a: int, b: int) -> int:
    """Example usage of decorator."""
    return a + b


if __name__ == "__main__":
    example(1, 2)
