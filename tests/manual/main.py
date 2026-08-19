import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src import PyHunters

pyhunters = PyHunters()


@pyhunters.mark("main")
def main():
    """Main function."""
    return 42


if __name__ == "__main__":
    main()
