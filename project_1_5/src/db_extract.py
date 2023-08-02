"""
    Python Real-World Projects
    Project 1.5: Acquire data from a SQL extract
"""
import model
import sqlite3
from typing import Any
from collections.abc import Iterator

class Extract:
    def build_samples(
            self,
            connection: sqlite3.Connection,
            config: dict[str, Any],
            name: str
    ) -> list[model.SeriesSample]:
        print(config['query']['samples'], {"name": name})
        samples_cursor = connection.execute(config['query']['samples'], {"name": name})
        samples = [
            model.SeriesSample(
                x=row[0],
                y=row[1])
            for row in samples_cursor
        ]
        return samples

    def series_iter(
            self,
            connection: sqlite3.Connection,
            config: dict[str, Any]
    ) -> Iterator[model.Series]:
        print(config['query']['names'])
        names_cursor = connection.execute(config['query']['names'])
        for row in names_cursor:
            name=row[0]
            yield model.Series(
                name=name,
                samples=self.build_samples(connection, config, name)
            )
