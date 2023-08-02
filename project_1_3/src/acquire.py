"""
    Python Real-World Projects
    Project 1.3: Scrape data from a web page
"""

import argparse
import logging
from pathlib import Path
import sys
import html_extract

logger = logging.getLogger("acquire")

def dump_table(url: str, caption: str):
    soup = html_extract.get_page(url)
    table_tag = html_extract.find_table_caption(soup, caption)
    source = iter(
        html_extract.table_row_data_iter(table_tag)
    )
    empty = next(source)
    header = next(source)
    logging.info("header: %r", header)
    count = 0
    for row in source:
        count += 1
        logging.info(row)
    logging.info("count: %d", count)

def get_options(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("-p", "--page", type=str)
    parser.add_argument("-c", "--caption", default="Anscombe's quartet")
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> None:
    options = get_options(argv or sys.argv[1:])
    dump_table(options.page, options.caption)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
