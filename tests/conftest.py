"""Pytest configuration and fixtures."""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app as flask_app


@pytest.fixture
def app():
    """Create and configure a test instance of the Flask app."""
    flask_app.config["TESTING"] = True
    flask_app.config["DEBUG"] = False
    yield flask_app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
