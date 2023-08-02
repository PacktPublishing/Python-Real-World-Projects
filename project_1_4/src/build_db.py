"""
    Python Real-World Projects
    Project 1.4: Local SQL Database
"""
import sqlite3
try:
    import tomllib  # type: ignore[import]
except ImportError:
    # Python < 3.11 requires an install of toml==0.10.2
    import toml as tomllib  # type: ignore[import]
from pathlib import Path
import csv
from typing import Any
from dataclasses import dataclass, asdict

def execute_statements(
        connection: sqlite3.Connection,
        statements: list[str] | str) -> None:
    match statements:
        case list(str):
            pass
        case str:
            statements = [statements]

    for statement in statements:
        try:
            cursor = connection.execute(statement)
            # Queries have rows...
            for row in cursor:
                print(row)
        except sqlite3.OperationalError:
            print("FAILURE")
            print(statement)
            raise
    connection.commit()

SERIES_ROWS = [
    {"series_id": 1, "name": "Series I"},
    {"series_id": 2, "name": "Series II"},
    {"series_id": 3, "name": "Series III"},
    {"series_id": 4, "name": "Series IV"},
]

@dataclass
class XYPair:
    x: str
    y: str

def series_1(row: dict[str, str]) -> XYPair:
    return XYPair(
        x=row['x123'],
        y=row['y1'],
    )

def series_2(row: dict[str, str]) -> XYPair:
    return XYPair(
        x=row['x123'],
        y=row['y2'],
    )

def series_3(row: dict[str, str]) -> XYPair:
    return XYPair(
        x=row['x123'],
        y=row['y3'],
    )

def series_4(row: dict[str, str]) -> XYPair:
    return XYPair(
        x=row['x4'],
        y=row['y4']
    )

SERIES_BUILDERS = [
    (1, series_1),
    (2, series_2),
    (3, series_3),
    (4, series_4)
]

def load_values(
        connection: sqlite3.Connection,
        insert_values_SQL: str,
        reader: csv.DictReader) -> None:

    for sequence, row in enumerate(reader):
        for series_id, extractor in SERIES_BUILDERS:
            param_values = (
                asdict(extractor(row)) | {"series_id": series_id, "sequence": sequence}
            )
            connection.execute(insert_values_SQL, param_values)
    connection.commit()

def schema_build_load(
        connection: sqlite3.Connection,
        config: dict[str, Any],
        data_source: Path
    ) -> None:
    execute_statements(connection, config['definition']['drop'])
    execute_statements(connection, config['definition']['create'])

    insert_series_SQL = config['manipulation']['insert_series']
    for series in SERIES_ROWS:
        connection.execute(insert_series_SQL, series)
    connection.commit()

    insert_values_SQL = config['manipulation']['insert_values']
    with data_source.open() as data_file:
        reader = csv.DictReader(data_file)
        load_values(connection, insert_values_SQL, reader)

    execute_statements(connection, config['query']['summary'])
    # execute_statements(connection, config['query']['detail'])

def main():
    config_path = Path.cwd() / "schema.toml"
    with config_path.open() as config_file:
        config = tomllib.load(config_file)

    data_path = Path.cwd().parent / "data" / "Anscombe_quartet_data.csv"
    with sqlite3.connect("file:example.db", uri=True) as connection:
        schema_build_load(connection, config, data_path)


if __name__ == "__main__":
    main()
