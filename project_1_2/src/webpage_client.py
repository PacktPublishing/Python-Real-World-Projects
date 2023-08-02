"""
    Python Real-World Projects
    Project 1.2: Acquire data from web service
"""
from collections.abc import Iterator
from urllib.request import urlopen

from bs4 import BeautifulSoup, Tag


def get_page(url: str) -> BeautifulSoup:
    return BeautifulSoup(
        urlopen(url), "html.parser"
    )

def find_table_caption(
        soup: BeautifulSoup,
        caption_text: str = "Anscombe's quartet"
    ) -> Tag:
    for table in soup.find_all('table'):
        if table.caption:
            if table.caption.text.strip() == caption_text.strip():
                return table
    raise RuntimeError(f"<table> with caption {caption_text!r} not found")

def extract_rows(table: Tag) -> Iterator[list[str]]:
    for tr in table.tbody.find_all('tr'):
        values = [td.text.strip() for td in tr.find_all('td')]
        yield values

def from_wikipedia():
    url = "https://en.wikipedia.org/wiki/Anscombe%27s_quartet"
    page_soup = get_page(url)
    table = find_table_caption(page_soup, "Anscombe's quartet")
    for row in extract_rows(table):
        print(row)

if __name__ == "__main__":
    from_wikipedia()
