"""
    Python Real-World Projects
    Project 1.3: Scrape data from a web page
"""

import html_extract
from pytest import fixture
from textwrap import dedent

@fixture
def example_1(tmp_path):
    html_page = tmp_path / "works.html"
    html_page.write_text(
        dedent("""
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <p>Some Text</p>
        <table class="wikitable">
            <tbody>
            <tr><th>Wrong Table</th></tr>
            <tr><td>Wrong Table</td></tr>
            </tbody>
        </table>
        <table class="wikitable">
            <caption>Anscombe's quartet
            </caption>
            <tbody>
            <tr><th>Skip titles</th><th>In th tags</th></tr>
            <tr><td>Keep this</td><td>Data</td></tr>
            <tr><td>And this</td><td>Data</td></tr>
            </tbody>
        </body>
        </html>
        """
        )
    )
    yield f"file://{str(html_page)}"
    html_page.unlink()

def test_dump(example_1, capsys):
    html_extract.dump_table(example_1, "Anscombe's quartet")
    out, err = capsys.readouterr()
    assert out == "[]\n['Keep this', 'Data']\n['And this', 'Data']\n"

def test_steps(example_1):
    soup = html_extract.get_page(example_1)
    table_tag = html_extract.find_table_caption(soup, "Anscombe's quartet")
    rows = list(html_extract.table_row_data_iter(table_tag))
    assert rows == [
        [],
        ['Keep this', 'Data'],
        ['And this', 'Data'],
    ]
