from functools import wraps
from typing import Callable
from main.configuration import Configuration
import os

configuration = Configuration.from_toml()


def watch(
    *,
    path: str | None = None,
    ignore_errs: tuple[Exception] | None = None,
):
    # path = _conditionally_default_path(path, script)
    # ignore_errs = ignore_errs or tuple()

    def decorator(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt + ignore_errs as e:
                pass
            except Exception as e:
                print(e)
                # logic to track status
                pass

        return inner

    return decorator


# def _missing_args(ignore_errs) -> set[str] | None:
#     missing_args = {}
#     for arg in ignore_errs:
#         if not arg and not getattr(configuration, arg, None):
#             raise ValueError()


# def _conditionally_default_path(path: str | None, script: str) -> str:
#     if path:
#         return path

#     cwd = os.getcwd()
#     return os.path.join(cwd, "geo_table", script)
