import logging

logger = logging.getLogger(__name__)

DEFAULT_INDENT = " " * 2
LOG_PREFIX = "PYHUNTERS"


def friendly_view(obj: object, nested_level: int = 0, omit_none: bool = True) -> str:
    """Returns a friendly view of the object's attributes and their values."""
    indent = DEFAULT_INDENT * nested_level
    longest_key = len(max(obj.__dict__.keys(), key=len))
    result = f"--- {LOG_PREFIX} ---\n{obj.__class__}\n"

    for key, value in obj.__dict__.items():
        if omit_none and value is None and not key.startswith("__"):
            continue
        result += f"{indent}{key:<{longest_key}} -> {value}\n"

    return result
