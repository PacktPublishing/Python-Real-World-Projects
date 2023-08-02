"""
    Python Real-World Projects
    Project Zero: A template for other projects
"""

import argparse
import sys


def get_options(argv: list[str]) -> argparse.Namespace:
    """Parse command-line"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--who", "-w", type=str, default="World")
    return parser.parse_args(argv)

def greeting(who: str = "World") -> None:
    """Write greeting."""
    print(f"Hello, {who}!")

def main(argv: list[str] = sys.argv[1:]) -> None:
    """Get options and write greeting."""
    options = get_options(argv)
    greeting(options.who)

if __name__ == "__main__":
    main()
