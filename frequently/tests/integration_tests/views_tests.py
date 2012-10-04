"""
Tests for the models of the myapp application.

"""
from django.test import TestCase
from django.core.urlresolvers import reverse

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin
from frequently.models import Entry, Feedback
from frequently.tests.factories import EntryFactory, EntryCategoryFactory


class CategoryListViewTestCase(ViewTestMixin, TestCase):
    """Tests for CategoryListView view class."""
    def setUp(self):
        self.user = UserFactory()
        self.category_1 = EntryCategoryFactory()
        self.category_2 = EntryCategoryFactory()
        self.category_3 = EntryCategoryFactory()
        self.entry_1 = EntryFactory(votes=2, amount_of_views=500)
        self.entry_1.category.add(self.category_1)
        self.entry_2 = EntryFactory(votes=-4, amount_of_views=200)
        self.entry_2.category.add(self.category_1)
        self.entry_3 = EntryFactory(votes=3, amount_of_views=100)
        self.entry_3.category.add(self.category_1)
        self.entry_4 = EntryFactory(votes=7, amount_of_views=200)
        self.entry_4.category.add(self.category_2)
        self.entry_5 = EntryFactory(votes=2, amount_of_views=50)
        self.entry_5.category.add(self.category_2)

    def get_view_name(self):
        return 'frequently:category_list'

    def test_negative_feedback(self):
        self.should_be_callable_when_authenticated(self.user)
        data = {
            'down1': 'Foo',
        }
        resp = self.client.get(reverse('frequently:category_list'), data=data)
        self.assertEqual(resp.status_code, 200)
        data = {
            'down1': 'Foo',
            'remark': 'Bar',
        }
        resp = self.client.post(reverse('frequently:category_list'), data=data)
        self.assertEqual(Feedback.objects.get(pk=1).remark, 'Bar')

    def test_positive_feedback(self):
        self.should_be_callable_when_authenticated(self.user)
        data = {
            'up1': 'Foo',
        }
        resp = self.client.post(reverse('frequently:category_list'), data=data)
        self.assertEqual(len(Entry.objects.get(pk=self.entry_1.pk).feedback_set.all()), 1)


class CategoryDetailViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``CategoryDetailView`` generic view class."""
    def setUp(self):
        self.category = EntryCategoryFactory()

    def get_view_name(self):
        return 'frequently:category_detail'

    def get_view_kwargs(self):
        return {'pk': self.category.pk, 'slug': self.category.slug}

    def test_view(self):
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 200)


class EntryDetailViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``EntryDetailView`` generic view class."""
    def setUp(self):
        self.entry = EntryFactory()

    def get_view_name(self):
        return 'frequently:entry_detail'

    def get_view_kwargs(self):
        return {'pk': self.entry.pk, 'slug': self.entry.slug}

    def test_view(self):
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 200)


class EntryCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``EntryCreateView`` generic view class."""
    def setUp(self):
        self.user = UserFactory()

    def get_view_name(self):
        return 'frequently:submit_question'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.user)
        data = {
            'question': 'Foo',
        }
        resp = self.client.post(self.get_url(), data=data)
        self.assertRedirects(
            resp,
            reverse('frequently:category_list'),
            msg_prefix=('Should redirect to category list view.')
        )
