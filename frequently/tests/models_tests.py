"""
Tests for the models of the ``django-frequently`` app.

"""
from django.test import TestCase

from frequently.tests.factories import (
    EntryCategoryFactory,
    EntryFactory,
    FeedbackFactory,
)


class EntryCategoryTestCase(TestCase):
    """Tests for the ``EntryCategory`` model class."""
    def test_model(self):
        obj = EntryCategoryFactory()
        self.assertTrue(obj.pk)


class EntryTestCase(TestCase):
    """Tests for the ``Entry`` model class."""
    def test_model(self):
        obj = EntryFactory()
        self.assertTrue(obj.pk)


class FeedbackTestCase(TestCase):
    """Tests for the ``Feedback`` model class."""
    def test_model(self):
        obj = FeedbackFactory()
        self.assertTrue(obj.pk)
