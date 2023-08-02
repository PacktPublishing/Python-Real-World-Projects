"""
    Python Real-World Projects
    Project 1.5: Acquire data from a SQL extract
"""
import sqlite3
from typing import Any, cast
from unittest.mock import Mock, call, sentinel
from pytest import fixture
import db_extract
import model

@fixture
def mock_connection() -> sqlite3.Connection:
    names_cursor: list[tuple[Any, ...]] = [
        (sentinel.Name,)
    ]
    samples_cursor: list[tuple[Any, ...]]  = [
        (sentinel.X, sentinel.Y)
    ]
    query_to_cursor: dict[sentinel, list[tuple[Any, ...]]] = {
        sentinel.Names_Query: names_cursor,
        sentinel.Samples_Query: samples_cursor
    }

    connection = Mock(
        execute=Mock(
            side_effect=lambda query, param=None: query_to_cursor[query]
        )
    )
    return cast(sqlite3.Connection, connection)

@fixture
def mock_config():
    return {
        'query': {
            'names': sentinel.Names_Query,
            'samples': sentinel.Samples_Query,
        }
    }

def test_build_sample(
        mock_connection: sqlite3.Connection,
        mock_config: dict[str, Any]
):
    extract = db_extract.Extract()
    results = list(
        extract.series_iter(mock_connection, mock_config)
    )
    assert results == [
        model.Series(
            name=sentinel.Name,
            samples=[
               model.SeriesSample(sentinel.X, sentinel.Y)
            ]
        )
    ]
    assert cast(Mock, mock_connection).execute.mock_calls == [
        call(sentinel.Names_Query),
        call(sentinel.Samples_Query, {'name': sentinel.Name})
    ]
