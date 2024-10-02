from main import main


@main.watch()
def some_func():
    print("something is happening")
    return None
