"""
    Python Real-World Projects
    Project Zero: A template for other projects
"""
import hello_world

def test_hello_world(capsys):
	hello_world.main([])
	out, err = capsys.readouterr()
	assert "Hello, World!" in out
