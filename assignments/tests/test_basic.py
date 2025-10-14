"""
Sample test file to demonstrate pytest-django setup.
"""
import pytest
from django.test import Client


@pytest.mark.django_db
class TestAssignmentsApp:
    """Test cases for assignments app."""

    def test_app_exists(self):
        """Test that the assignments app is configured correctly."""
        from django.apps import apps
        assert apps.is_installed('assignments')

    def test_client_setup(self):
        """Test that Django test client works."""
        client = Client()
        assert client is not None
