"""
    Python Real-World Projects
    Project 1.3: Scrape data from a web page
"""
from behave import given, when, then
from pathlib import Path
import subprocess
import shlex
from textwrap import dedent

@given(u'an HTML page "{filename}"')
def step_impl(context, filename):
    # print(filename)
    context.path = Path(filename)
    context.path.write_text(dedent(context.text))
    context.add_cleanup(context.path.unlink)

@when(u'we run the html extract command')
def step_impl(context):
    command = [
        'python', 'src/acquire.py', '-o', 'quartet', '--page', '$URL', '--caption', "Anscombe's quartet"
    ]
    url = f"file://{str(context.path.absolute())}"
    command[command.index('$URL')] = url
    print(shlex.join(command))
    output_path = Path("output.log")
    with output_path.open('w') as target:
        status = subprocess.run(
            command,
            check=True, text=True, stdout=target, stderr=subprocess.STDOUT)
    context.status = status
    context.output = output_path.read_text()
    output_path.unlink()
    # print(f"{context=} {context.status=} {context.output=}")


@then(u'log has INFO line with "{log_line}"')
def step_impl(context, log_line):
    print(context.output)
    assert log_line in context.output, f"No {log_line!r} in output"
