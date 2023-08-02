"""
    Python Real-World Projects
    Project 1.5: Acquire data from a SQL extract
"""
import argparse
import csv
import sqlite3
try:
    import tomllib  # type: ignore[import]
except ImportError:
    # Python < 3.11 requires an install of toml==0.10.2
    import toml as tomllib  # type: ignore[import]
from pathlib import Path
from typing import Any
import sys

from db_extract import Extract

def get_options(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("-d", "--db_uri", default="file:example.db")
    parser.add_argument("-s", "--schema", type=Path, default="schema.toml")
    return parser.parse_args(argv)

def main(argv: list[str] = sys.argv[1:]) -> None:
    options = get_options(argv)
    with options.schema.open('rb') as config_file:  # 'rb' for tomllib and 3.11
        config = tomllib.load(config_file)
    print("config", config)
    print("db_uri", options.db_uri)

    extract = Extract()
    with sqlite3.connect(options.db_uri, uri=True) as connection:
        for s in extract.series_iter(connection, config):
            print(s)
            print(f"series: {s.name}\ncount: {len(s.samples)}")
            target = (options.output / s.name).with_suffix(".csv")
            print(f"Create {target}")
            with target.open('w', newline='') as output_file:
                writer = csv.DictWriter(output_file, ['x', 'y'])
                writer.writeheader()
                writer.writerows(
                    [{'x': sample.x, 'y': sample.y} for sample in s.samples]
                )

if __name__ == "__main__":
    main()
