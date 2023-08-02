"""
    Python Real-World Projects
    Project 1.1: Data Acquisition Base Application
"""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
from csv_extract import *

def get_options(argv: list[str]) -> argparse.Namespace:
    defaults = argparse.Namespace(
        extract_class=Extract,
        series_classes=[Series1Pair, Series2Pair, Series3Pair, Series4Pair],
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=Path, default="data")
    parser.add_argument('source', type=Path, nargs='*')
    return parser.parse_args(argv, defaults)


EXTRACT_CLASS: type[Extract] = Extract
BUILDER_CLASSES: list[type[PairBuilder]] = [Series1Pair, Series2Pair, Series3Pair, Series4Pair]

def main(argv: list[str]) -> None:
    builders = [cls() for vls in BUILDER_CLASSES]
    extractor = EXTRACT_CLASS(builders)
    # etc.

    options = get_options(argv)

    targets = [
        options.output / "Series_1.ndjson",
        options.output / "Series_2.ndjson",
        options.output / "Series_3.ndjson",
        options.output / "Series_4.ndjson",
    ]
    target_files = [
        target.open('w') for target in targets
    ]
    for source in options.source:
        with source.open() as source:
            rdr = csv.reader(source)
            for row in rdr:
                for row, wtr in zip(extractor.build_pairs(row), target_files):
                    wtr.write(json.dumps(asdict(row)) + '\n')
    for target in target_files:
        target.close()

if __name__ == "__main__":
    main()
