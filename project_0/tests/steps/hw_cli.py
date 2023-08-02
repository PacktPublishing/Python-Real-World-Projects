"""
    Python Real-World Projects
    Project Zero: A template for other projects
"""
import subprocess
import shlex
from pathlib import Path

@when(u'we run command "{command}"')
def step_impl(context, command):
    output_path = Path("output.log")
    with output_path.open('w') as target:
        status = subprocess.run(
            shlex.split(command),
            check=True, text=True, stdout=target, stderr=subprocess.STDOUT)
    context.status = status
    context.output = output_path.read_text()
    output_path.unlink()
    # print(f"{context=} {context.status=} {context.output=}")

@then(u'output has "{expected_output}"')
def step_impl(context, expected_output):
    # print(f"{context=} {context.status=} {context.output=}")
    assert context.status.returncode == 0
    assert expected_output in context.output
