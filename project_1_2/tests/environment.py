"""
    Python Real-World Projects
    Project 1.2: Acquire data from web service
"""
from collections.abc import Iterator
from typing import Any
import subprocess
import time
import os
import sys
from behave import fixture, use_fixture
from behave.runner import Context

@fixture
def kaggle_server(context: Context) -> Iterator[Any]:
    """
    Used by a Scenario (or Feature) to start the server running.
    """
    if "environment" not in context:
        context.environment = os.environ
    context.environment["ACQUIRE_BASE_URL"] = "http://127.0.0.1:8080"
    # Save server-side log for debugging
    server = subprocess.Popen(
        [sys.executable, "tests/mock_kaggle_bottle.py"],
    )
    time.sleep(0.5)  # 500 ms delay to allow service to open socket
    yield server
    server.kill()

def before_tag(context: Context, tag: str) -> None:
    """
    Expands a @fixture to invoke the appropriate generator.
    """
    if tag == "fixture.kaggle_server":
        # This will invoke the definition generator.
        # It consumes a value before and after the tagged scenario.
        use_fixture(kaggle_server, context)

def before_scenario(context, scenario):
    if "environment" not in context:
        context.environment = os.environ

def after_scenario(context, scenario):
    if "temp_path" in context:
        context.temp_path.unlink()
