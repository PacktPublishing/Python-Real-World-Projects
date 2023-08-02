"""
    Python Real-World Projects
    Project 1.1: Data Acquisition Base Application
"""

from unittest.mock import sentinel
from dataclasses import asdict

from model import XYPair

def test_xypair():
    pair = XYPair(x=sentinel.X, y=sentinel.Y)
    assert pair.x == sentinel.X
    assert pair.y == sentinel.Y
    assert asdict(pair) == {"x": sentinel.X, "y": sentinel.Y}
