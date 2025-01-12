from src import getWatcher

watcher = getWatcher()


def main():
    ans = 1 + 1
    watcher.add(ans, 2)
    breakpoint()


if __name__ == "__main__":
    main()
