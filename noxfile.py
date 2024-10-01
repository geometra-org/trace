import nox

@nox.session(python="3.12")
def generate_requirements(session: nox.Session) -> None:
    """Generate a `requirements.txt` from root level `pyproject.toml`"""
    session.install("pip-tools")
    session.run(*["pip-compile", "--output-file=requirements.txt", "pyproject.toml"])
