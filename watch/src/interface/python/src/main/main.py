from functools import wraps
from typing import Callable
from .configuration import Configuration
from .session import Session
from .export import Exportinator
from .relation import Relation

# configuration = Configuration.from_toml()


def watch(
    *,
    path: str | None = None,
    ignore_errs: tuple[Exception] | None = None,
):
    # path = _conditionally_default_path(path, script)
    # ignore_errs = ignore_errs or tuple()
    # exporter = Exportinator.from_path(path)

    def decorator(func: Callable):
        session = Session.from_call(func)

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                with session:
                    return func(*args, **kwargs)
            except KeyboardInterrupt + ignore_errs as e:
                pass
            except Exception as e:
                print(e)
                # logic to track status
                pass

        breakpoint()
        relation = Relation.from_session(session)

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
