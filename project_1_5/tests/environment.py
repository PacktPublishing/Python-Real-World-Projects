"""
    Python Real-World Projects
    Project 1.5: Acquire data from a SQL extract
"""
from collections.abc import Iterator
from pathlib import Path
import shutil
import sqlite3
from tempfile import mkdtemp
try:
    import tomllib  # type: ignore[import]
except ImportError:
    # Python < 3.11 requires an install of toml==0.10.2
    import toml as tomllib  # type: ignore[import]

from behave import fixture, use_fixture
from behave.runner import Context

@fixture
def sqlite_database(context: Context) -> Iterator[str]:
    # Get Config with SQL to build schema.
    config_path = Path.cwd() / "schema.toml"
    with config_path.open('rb') as config_file:  # 'rb' for tomllib and 3.11
        config = tomllib.load(config_file)
        create_sql = config['definition']['create']
        context.manipulation_sql = config['manipulation']
    # Build database file.
    context.working_path = Path(mkdtemp())
    context.db_path =  context.working_path / "test_example.db"
    context.db_uri = f"file:{context.db_path}"
    context.connection = sqlite3.connect(context.db_uri, uri=True)
    for stmt in create_sql:
        context.connection.execute(stmt)
    context.connection.commit()

    # Yield to allow scenario to run.
    yield context.db_uri

    # Delete DB (and output files) after scenario is completed.
    context.connection.close()
    shutil.rmtree(context.working_path)
    assert not context.working_path.exists(), f"Files in {context.working_path} not removed"

def before_tag(context: Context, tag: str) -> None:
    """
    Expands a @fixture to invoke the appropriate generator.
    """
    if tag == "fixture.sqlite":
        # This will invoke the definition generator.
        # It consumes a value before and after the tagged scenario.
        use_fixture(sqlite_database, context)
