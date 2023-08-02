"""
    Python Real-World Projects
    Project 1.5: Acquire data from a SQL extract
"""
from behave import given, when, then
from ast import literal_eval
import subprocess
import shlex
from pathlib import Path
import textwrap

@given(u'a series named "{name}"')
def step_impl(context, name):
    insert_series = context.manipulation_sql['insert_series']
    cursor = context.connection.execute(
        insert_series,
        {'series_id': 99, 'name': name}
    )
    # DEBUG: print(f"Loaded series {name}: {cursor.rowcount}")
    context.connection.commit()


@given(u'sample values "{list_of_pairs}"')
def step_impl(context, list_of_pairs):
    pairs = literal_eval(list_of_pairs)
    insert_values = context.manipulation_sql['insert_values']
    for seq, row in enumerate(pairs):
        cursor = context.connection.execute(
            insert_values,
            {'series_id': 99, 'sequence': seq, 'x': row[0], 'y': row[1]}
        )
        # DEBUG: print(f"Loaded pairs {row}", cursor.rowcount)
    context.connection.commit()


@when(u'we run the database extract command with the test fixture database')
def step_impl(context):
    output_path = context.working_path / "quartet"
    output_path.mkdir()
    command = f"python src/acquire.py -o '{output_path!s}' --db_uri '{context.db_uri!s}' --schema schema.toml"
    output_path = Path("output.log")
    with output_path.open('w') as target:
        status = subprocess.run(
            shlex.split(command),
            # check=True,  # Makes debugging awkward
            text=True, stdout=target, stderr=subprocess.STDOUT)
    context.status = status
    context.output = output_path.read_text()
    output_path.unlink()
    # print(f"{context=} {context.status=} {context.output=}")


@then(u'log has INFO line with "{log_line}"')
def step_impl(context, log_line):
    print("Log Output:")
    print(textwrap.indent(context.output, '| '))
    assert log_line in context.output, f"No {log_line!r} in output"


@then(u'output directory has file named "{output_name}"')
def step_impl(context, output_name):
    output_path = context.working_path / output_name
    assert output_path.exists() and output_path.is_file(), f"No {output_name} file found"
