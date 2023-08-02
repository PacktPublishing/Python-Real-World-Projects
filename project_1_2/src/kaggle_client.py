"""
    Python Real-World Projects
    Project 1.2: Acquire data from web service
"""
from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
import io
import json
import logging
from pathlib import Path
from pprint import pprint
from textwrap import shorten
import zipfile

from bs4 import BeautifulSoup
from model import RawData, XYPair

# Option 1: Static Dependency
# import requests
# import requests.auth

# Option 2: Dependency Injection
import importlib
# Can be changed for testing
requests_name = "requests"
requests = importlib.import_module(requests_name)


class PairBuilder(ABC):
    target_class: type[RawData]

    @abstractmethod
    def from_row(self, row: list[str]) -> RawData:
        ...

@dataclass
class Dataset:
    title: str
    ref: str
    url: str
    totalBytes: int
    viewCount: int
    voteCount: int
    downloadCount: int
    usabilityRating: float

class DSBuilder:
    target_class: type[Dataset] = Dataset

    def from_json(self, obj: dict[str, str]) -> "Dataset":
        return self.target_class(
            title=obj['title'],
            ref=obj['ref'],
            url=obj['url'],
            totalBytes=int(obj['totalBytes']),
            viewCount=int(obj['viewCount']),
            voteCount=int(obj['voteCount']),
            downloadCount=int(obj['downloadCount']),
            usabilityRating=int(obj['usabilityRating']),
        )


class RestAccess:
    logger: logging.Logger = logging.getLogger("RestAccess")

    def __init__(self, kaggle_doc: dict[str, str]) -> None:
        self.credentials = requests.auth.HTTPBasicAuth(
            kaggle_doc['username'], kaggle_doc['key']
        )

    @staticmethod
    def error_dump(prefix: str, response: requests.Response) -> None:
        RestAccess.logger.debug("%s %r", prefix, response)
        RestAccess.logger.debug("Query: %s %s", response.request.method, response.request.url)
        for k, v in response.headers.items():
            RestAccess.logger.debug("  %r: %r", k, shorten(v, 128))
        RestAccess.logger.debug(response.content)

    def get_paged_json(
            self,
            url: str,
            query: dict[str, str] | None = None
    ) -> Iterator[dict[str, str]]:
        """Paginated requests, e.g., datasets/list"""
        query = {} if query is None else query
        page = 1
        while True:
            response = requests.get(
                url,
                auth=self.credentials,
                params=query | {'page': str(page)},
                headers={"Accept": "application/json"},
            )
            self.error_dump(f"{url}", response)
            if response.status_code == 200:
                details = response.json()
                if details:
                    yield from iter(details)
                    page += 1
                else:
                    RestAccess.logger.info("Final Content: %r", response.content)
                    break  # No more data.
            else:
                # Unexpected response, e.g., a 429 Too Many Requests
                RestAccess.logger.error("Page %d", page)
                self.error_dump(f"UNEXPECTED", response)
                break

    def get_json(self, url: str, params: dict[str, str] | None = None) -> dict[str, any]:
        mime_type = "application/json"
        response = requests.get(url, auth=self.credentials, params=params, headers={"Accept": mime_type})
        if response.status_code == 200:
            if response.headers.get('Content-Type', 'plain/text').startswith(mime_type):
                return response.json()
            else:
                self.error_dump(f"NOT {mime_type}", response)
        else:
            self.error_dump(f"UNEXPECTED", response)

    def get_html(self, url: str, params: dict[str, str] | None = None) -> bytes:
        mime_type = "text/html"
        response = requests.get(url, auth=self.credentials, params=params, headers={"Accept": mime_type})
        if response.status_code == 200:
            if response.headers.get('Content-Type', 'plain/text').startswith(mime_type):
                return response.content
        self.error_dump(f"UNEXPECTED", response)

    def get_zip(self, url: str, params: dict[str, str] | None = None) -> zipfile.ZipFile:
        mime_type = "application/zip"
        response = requests.get(url, auth=self.credentials, params=params, headers={"Accept": mime_type})
        if response.status_code == 200:
            self.error_dump(f"{url}", response)
            if response.headers.get('Content-Type', 'plain/text').startswith(mime_type):
                content = io.BytesIO(response.content)
                zip_file = zipfile.ZipFile(content)
                return zip_file
            else:
                self.error_dump(f"NOT {mime_type}", response)
        else:
            self.error_dump(f"UNEXPECTED", response)

    def close(self):
        pass

class RestExtract:
    def __init__(self, builders: list[PairBuilder]) -> None:
        self.builders = builders

    def build_pairs(self, row: list[str]) -> list[RawData]:
        return [bldr.from_row(row) for bldr in self.builders]

### SPIKE SOLUTIONS

def find_json() -> None:
    keypath = Path.home()/"Downloads"/"kaggle.json"
    with keypath.open() as keyfile:
        credentials = json.load(keyfile)
    reader = RestAccess(credentials)

    builder = DSBuilder()
    list_url = "https://www.kaggle.com/api/v1/datasets/list"
    query = {"filetype": "json", "maxSize": 1_000_000, "group": "public"}
    count = 0
    for row in reader.get_paged_json(list_url, query):
        count += 1
        ds = builder.from_json(row)
        if ds.usabilityRating > 0.5:
            print(ds)
    print(f"Found {count} datasets")

def main(argv: list[str] | None = None) -> None:
    keypath = Path.home()/"Downloads"/"kaggle.json"
    with keypath.open() as keyfile:
        credentials = json.load(keyfile)
    reader = RestAccess(credentials)

    data_url = None
    data_ref = None
    list_url = "https://www.kaggle.com/api/v1/datasets/list"
    for row in reader.get_paged_json(list_url, {"user": "carlmcbrideellis"}):
        print(row['title'], row['ref'], row['url'], row['totalBytes'])
        if "Anscombe" in row['title']:
            data_ref = row['ref']
            data_url = row['url']
            currentVersionNumber = row['currentVersionNumber']
            pprint(row)

    # An HTML page about the dataaset.
    # url = 'https://www.kaggle.com/datasets/carlmcbrideellis/data-anscombes-quartet'
    print()
    print(f"DATASET PAGE: {data_url}")
    soup = BeautifulSoup(reader.get_html(data_url), "html.parser")
    for script in soup.head.find_all("script"):
        if script.attrs.get("type") == "application/ld+json":
            print(script.attrs)
            content_object = json.loads(script.text)
            pprint(content_object)
    print()

    # Metadata
    # url = "https://www.kaggle.com/datasets/metadata/{ownerSlug}/{datasetSlug}"
    metadata_url = f'https://www.kaggle.com/api/v1/datasets/metadata/{data_ref}'
    print()
    print(f"METADATA PAGE: {data_url}")
    metadata_page = reader.get_json(metadata_url)
    pprint(metadata_page)
    print()

    # The downloadable data
    # From the metadata page...
    # HTML url = "https://www.kaggle.com/datasets/carlmcbrideellis/data-anscombes-quartet/download?datasetVersionNumber=1"
    # url = "https://www.kaggle.com/api/v1/datasets/download/{ownerSlug}/{datasetSlug}
    download_url = f'https://www.kaggle.com/api/v1/datasets/download/{data_ref}'

    series_1 = None # PairBuilder()
    extractor = RestExtract([series_1])
    print()
    print(f"DATA: {download_url!r}")
    zip_data = reader.get_zip(download_url, params={"datasetVersionNumber": currentVersionNumber})
    print(zip_data)
    print(zip_data.infolist())
    with zip_data.open("Anscombe_quartet_data.csv") as quartet_data:
        for line in quartet_data:
            print(line)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    # find_json()
