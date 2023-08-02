"""
    Python Real-World Projects
    Project 1.2: Acquire data from web service
"""
import argparse
import csv
import json
import logging
import os
from pathlib import Path
import sys
import zipfile
from model import *
from kaggle_client import RestAccess

logger = logging.getLogger("acquire")

def get_options(argv: list[str]) -> argparse.Namespace:
    base_url = os.environ.get("ACQUIRE_BASE_URL", "https://www.kaggle.com")
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("-k", "--key", type=Path)
    parser.add_argument("-z", "--zip", default="carlmcbrideellis/data-anscombes-quartet")
    parser.add_argument("-b", "--baseurl", default=base_url)
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> None:
    options = get_options(argv or sys.argv[1:])
    if options.key:
        with options.key.open() as key_file:
            credentials = json.load(key_file)
    else:
        logger.error("No credentials file provided on command line.")
        sys.exit(2)

    access = RestAccess(credentials)
    base_url = options.baseurl
    ref = options.zip
    download_url = f"{base_url}/api/v1/datasets/download/{ref}"
    logger.info("Downloading %s", download_url)
    member_name = "Anscombe_quartet_data.csv"
    logger.info("Opening %s", member_name)

    zip_data = access.get_zip(download_url)
    if member_name not in zip_data.namelist():
        logger.error("Could not find %s in %s", member_name, zip_data.infolist())
    count = 0
    zp = zipfile.Path(zip_data, member_name)
    with zp.open('r') as quartet_data:
        reader = csv.DictReader(quartet_data)
        logger.info("header: %s", reader.fieldnames)
        for line in reader:
            logger.debug(line)
            count += 1
    logger.info("count: %d", count)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
