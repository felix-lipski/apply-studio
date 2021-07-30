from blessed import Terminal
from loop import input_loop
from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser(description='TUI inteface for job sites.')
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--offline", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    term = Terminal()
    print(term.clear)
    input_loop(term, **vars(args))
