"""
    Python Real-World Projects
    Project 1.3: Scrape data from a web page
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup, Tag
from collections.abc import Iterator

def get_page(url: str) -> BeautifulSoup:
    return BeautifulSoup(
        urlopen(url), "html.parser"
    )

def find_table_caption(soup: BeautifulSoup, caption_text: str = "Anscombe's quartet") -> Tag:
    for table in soup.find_all('table'):
        if table.caption:
            if table.caption.text.strip() == caption_text.strip():
                return table
    raise RuntimeError(f"<table> with <caption>{caption_text}</caption> not found")

def table_row_data_iter(table: Tag) -> Iterator[list[str]]:
    for row in table.tbody.find_all('tr'):
        flat = [td.text.strip() for td in row.find_all('td')]
        yield flat

def dump_table(url: str, caption: str):
    soup = get_page(url)
    table_tag = find_table_caption(soup, caption)
    for row in table_row_data_iter(table_tag):
        print(row)

if __name__ == "__main__":
    dump_table("https://en.wikipedia.org/wiki/Anscombe's_quartet", "Anscombe's quartet")
