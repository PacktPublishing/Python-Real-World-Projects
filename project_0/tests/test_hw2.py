"""
    Python Real-World Projects
    Project Zero: A template for other projects
"""
import pytest

import hw2

@pytest.mark.xfail(reason="Not fully implemented")
def test_hw2(capsys):
	hw2.main([])
	out, err = capsys.readouterr()
	assert "Hello, World!" in out
