"""
    Python Real-World Projects
    Project 1.4: Local SQL Database
"""
from unittest.mock import MagicMock, Mock, call, sentinel
from pytest import fixture
import build_db

@fixture
def mock_connection():
    mock_cursor = []
    mock_connection = Mock(
        name='connection',
        execute=Mock(return_value=mock_cursor)
    )
    return mock_connection

def test_execute_statements(mock_connection):
    build_db.execute_statements(mock_connection, [sentinel.S1, sentinel.S2])
    assert mock_connection.execute.mock_calls == [
        call(sentinel.S1),
        call(sentinel.S2)
    ]

@fixture
def mock_query_connection():
    mock_cursor = [sentinel.ROW]
    mock_connection = Mock(
        name='connection',
        execute=Mock(return_value=mock_cursor)
    )
    return mock_connection

def test_execute_statements_query(mock_query_connection, capsys):
    build_db.execute_statements(mock_query_connection, sentinel.QUERY)
    assert mock_query_connection.execute.mock_calls == [
        call(sentinel.QUERY),
    ]
    output, error = capsys.readouterr()
    assert output.splitlines() == [
        'sentinel.ROW'
    ]
