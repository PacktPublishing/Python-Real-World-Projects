"""
    Python Real-World Projects
    Project 1.5: Acquire data from a SQL extract
"""
from dataclasses import dataclass

@dataclass
class SeriesSample:
    x: str
    y: str

@dataclass
class Series:
    name: str
    samples: list[SeriesSample]
