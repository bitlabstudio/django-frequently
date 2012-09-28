"""
Tests for the models of the ``django-frequently`` app.

"""
from django.test import TestCase

from frequently.tests.factories import ExampleFactory


class ExampleTestCase(TestCase):
    """Tests for the ``Example`` model class."""
    def test_model(self):
        obj = ExampleFactory()
        self.assertTrue(obj.pk)
