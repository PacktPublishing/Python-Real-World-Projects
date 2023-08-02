"""
    Python Real-World Projects
    Project 1.2: Acquire data from web service
"""
from behave import *
from urllib.parse import urlparse
from pathlib import Path
import json
import subprocess
import shlex

@given(u'proper keys are in "{local_path_str}"')
def step_impl(context, local_path_str):
    proper_keys = {'username': 'test', 'key': 'some-hex-string'}
    temp_path = Path(local_path_str)
    with temp_path.open('w') as output:
        json.dump(proper_keys, output)
    context.temp_path = temp_path


@when(u'we run the kaggle download command')
def step_impl(context):
    command = "python src/acquire.py -k kaggle.json -o quartet --zip carlmcbrideellis/data-anscombes-quartet"
    # print(f"{context.environment=}")
    output_path = Path("output.log")
    with output_path.open('w') as target:
        status = subprocess.run(
            shlex.split(command),
            env=context.environment,
            check=True, text=True, stdout=target, stderr=subprocess.STDOUT)
    context.status = status
    context.output = output_path.read_text()
    output_path.unlink()
    # print(f"{context=} {context.status=} {context.output=}")


@then(u'log has INFO line with "{log_line}"')
def step_impl(context, log_line):
    print(context.output)
    assert log_line in context.output, f"No {log_line!r} in output"

@when(u'we run the html extract command')
def step_impl(context):
    command = [
        'python', 'src/acquire.py',
        '-o', 'quartet',
        '--page', '$URL',
        '--caption', "Anscombe's quartet"
    ]
    url = f"file://{str(context.path.absolute())}"
    command[command.index('$URL')] = url
    print(shlex.join(command))
    # etc. with subprocess.run() to execute the command
