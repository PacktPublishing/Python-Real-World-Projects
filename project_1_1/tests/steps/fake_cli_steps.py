"""
    Python Real-World Projects
    Project 1.1: Data Acquisition Base Application
"""

# These step definitions will "pass" a test run.
# These serve to confirm the Feature file syntax.

@given(u'the "Anscombe_quartet_data.csv" source file exists')
def step_impl(context):
    pass  # raise NotImplementedError(u'STEP: Given the "Anscombe_quartet_data.csv" source file exists')


@given(u'the "quartet" directory exists')
def step_impl(context):
    pass  # raise NotImplementedError(u'STEP: Given the "quartet" directory exists')


@when(u'we run command "python src/acquire.py -o quartet Anscombe_quartet_data.csv"')
def step_impl(context):
    pass  # raise NotImplementedError(u'STEP: When we run command "python src/acquire.py -o quartet Anscombe_quartet_data.csv"')


@then(u'the "quartet/series_1.json" file exists')
def step_impl(context):
    pass  # raise NotImplementedError(u'STEP: Then the "quartet/series_1.json" file exists')


@then(u'the "quartet/series_2.json" file exists')
def step_impl(context):
    pass  # raise NotImplementedError(u'STEP: Then the "quartet/series_2.json" file exists')


@then(u'the "quartet/series_3.json" file exists')
def step_impl(context):
    pass  # raise NotImplementedError(u'STEP: Then the "quartet/series_3.json" file exists')


@then(u'the "quartet/series_1.json" file starts with \'{"x": "10.0", "y": "8.04"}\'')
def step_impl(context):
    pass  # raise NotImplementedError(u'STEP: Then the "quartet/series_1.json" file starts with \'{"x": "10.0", "y": "8.04"}\'')


@given(u'the "Anscombe_quartet_data.csv" source file does not exist')
def step_impl(context):
    pass  # raise NotImplementedError(u'STEP: Given the "Anscombe_quartet_data.csv" source file does not exist')


@then(u'the log contains "File not found: Anscombe_quartet_data.csv"')
def step_impl(context):
    pass  # raise NotImplementedError(u'STEP: Then the log contains "File not found: Anscombe_quartet_data.csv"')

