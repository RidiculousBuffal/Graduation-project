# tests/conftest.py
import pytest
from app import create_app
from app.ext.extensions import db


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')

    # Create an application context
    with app.app_context():
        # Create all tables
        db.create_all()
        yield app
        # Clean up after the test
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()