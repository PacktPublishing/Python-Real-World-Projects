"""
    Python Real-World Projects
    Project Zero: A template for other projects
"""

"""
A skeleton to show our initial thoughts on a functional design.
"""

import argparse
import sys


def get_options(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    """Parse command-line"""
    pass

def greeting(who: str = "World") -> None:
    """Write greeting."""
    print(f"Hello, {who}!")

def main(argv: list[str] = sys.argv[1:]) -> None:
    """Get options and write greeting."""
    pass

if __name__ == "__main__":
    main()
