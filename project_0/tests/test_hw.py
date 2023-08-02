"""
    Python Real-World Projects
    Project Zero: A template for other projects
"""
import pytest

import hw

@pytest.mark.xfail(reason="Not fully implemented")
def test_hw(capsys):
	hw.main([])
	out, err = capsys.readouterr()
	assert "Hello, World!" in out
