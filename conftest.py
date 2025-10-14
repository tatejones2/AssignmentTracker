"""
Pytest configuration file for Django testing.
"""
import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    """
    Configure the database for testing.
    Uses SQLite in-memory database for fast tests.
    """
    pass


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Give all tests access to the database.
    """
    pass
