"""
    Python Real-World Projects
    Project 1.1: Data Acquisition Base Application
"""
from model import RawData, XYPair
from abc import ABC, abstractmethod
import csv
from pathlib import Path


class PairBuilder(ABC):
    target_class: type[RawData]

    @abstractmethod
    def from_row(self, row: list[str]) -> RawData:
        ...


class Series1Pair(PairBuilder):
    target_class = XYPair

    def from_row(self, row: list[str]) -> RawData:
        cls = self.target_class
        # the rest of the implementation...
        return cls(row[0], row[1])

class Series2Pair(PairBuilder):
    target_class = XYPair

    def from_row(self, row: list[str]) -> RawData:
        cls = self.target_class
        return cls(row[0], row[2])

class Series3Pair(PairBuilder):
    target_class = XYPair

    def from_row(self, row: list[str]) -> RawData:
        cls = self.target_class
        return cls(row[0], row[3])

class Series4Pair(PairBuilder):
    target_class = XYPair

    def from_row(self, row: list[str]) -> RawData:
        cls = self.target_class
        return cls(row[4], row[5])

class Extract:
    def __init__(self, builders: list[PairBuilder]) -> None:
        self.builders = builders

    def build_pairs(self, row: list[str]) -> list[RawData]:
        return [bldr.from_row(row) for bldr in self.builders]

EXTRACT_CLASS: type[Extract] = Extract
BUILDER_CLASSES: list[type[PairBuilder]] = [Series1Pair,]

def test_series1pair() -> None:
    from unittest.mock import Mock, sentinel, call
    mock_raw_class = Mock()
    p1 = Series1Pair()
    p1.target_class = mock_raw_class
    xypair = p1.from_row([sentinel.X, sentinel.Y])
    assert mock_raw_class.mock_calls == [
        call(sentinel.X, sentinel.Y)
    ]
