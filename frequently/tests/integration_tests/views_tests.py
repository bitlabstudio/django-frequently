"""
Tests for the models of the myapp application.

"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin
from frequently.models import Entry, Feedback
from frequently.tests.factories import (
    EntryFactory,
    EntryCategoryFactory,
    FeedbackFactory,
)


class CategoryListViewTestCase(ViewTestMixin, TestCase):
    """Tests for CategoryListView view class."""
    def setUp(self):
        self.user = UserFactory()
        self.category_1 = EntryCategoryFactory()
        self.category_2 = EntryCategoryFactory()
        self.category_3 = EntryCategoryFactory()
        self.entry_1 = EntryFactory(upvotes=2, amount_of_views=500)
        self.entry_1.category.add(self.category_1)
        self.entry_2 = EntryFactory(downvotes=4, amount_of_views=200)
        self.entry_2.category.add(self.category_1)
        self.entry_3 = EntryFactory(upvotes=3, amount_of_views=100)
        self.entry_3.category.add(self.category_1)
        self.entry_4 = EntryFactory(upvotes=7, amount_of_views=200)
        self.entry_4.category.add(self.category_2)
        self.entry_5 = EntryFactory(upvotes=2, amount_of_views=50)
        self.entry_5.category.add(self.category_2)

    def get_view_name(self):
        return 'frequently_category_list'

    def test_positive_feedback(self):
        data = {
            'up%d' % self.entry_1.pk: 'Foo',
            'user_id': self.user.pk
        }
        self.client.post(self.get_url(), data=data)
        self.assertEqual(len(Entry.objects.get(
            pk=self.entry_1.pk).feedback_set.all()), 1)

    def test_negative_feedback(self):
        self.should_be_callable_when_authenticated(self.user)
        data = {
            'down%d' % self.entry_1.pk: 'Foo',
            'user_id': self.user.pk
        }
        self.client.post(self.get_url(), data=data)
        self.assertEqual(Feedback.objects.get(pk=1).validation, 'N')

    def test_positive_feedback_with_ajax(self):
        data = {
            'up%d' % self.entry_1.pk: 'Foo',
            'user_id': '55555'
        }
        self.client.post(
            self.get_url(),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(len(Entry.objects.get(
            pk=self.entry_1.pk).feedback_set.all()), 1)
        data = {
            'up%d' % self.entry_1.pk: 'Foo',
            'user_id': 'test'
        }
        self.client.post(
            self.get_url(),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(len(Entry.objects.get(
            pk=self.entry_1.pk).feedback_set.all()), 1)

    def test_negative_feedback_with_ajax(self):
        data = {
            'down%d' % self.entry_1.pk: 'Foo',
        }
        self.client.post(
            self.get_url(),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(Feedback.objects.get(pk=1).validation, 'N')

    def test_rating_refresh_ajax_request(self):
        data = {
            'ratingID': 'ratingID%s' % self.entry_1.pk,
        }
        resp = self.client.post(
            self.get_url(),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(resp.content, '%s' % self.entry_1.rating())

    def test_feedback_submission_with_ajax(self):
        feedback = FeedbackFactory()
        remark = 'Your app is beautiful'
        data = {
            'feedback%d' % feedback.pk: True,
            'remark': remark,
        }
        self.client.post(
            self.get_url(),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(Feedback.objects.get(pk=feedback.pk).remark, remark)

    def test_last_view_date_with_ajax(self):
        data = {
            'refresh_last_view': self.entry_1.pk,
        }
        self.client.post(
            self.get_url(),
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertGreater(
            Entry.objects.get(pk=self.entry_1.pk).last_view_date,
            self.entry_1.last_view_date,
        )


class CategoryDetailViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``CategoryDetailView`` generic view class."""
    def setUp(self):
        self.category = EntryCategoryFactory()

    def get_view_name(self):
        return 'frequently_category_detail'

    def get_view_kwargs(self):
        return {'pk': self.category.pk, 'slug': self.category.slug}

    def test_view(self):
        self.should_be_callable_when_anonymous()


class EntryDetailViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``EntryDetailView`` generic view class."""
    def setUp(self):
        self.entry = EntryFactory()

    def get_view_name(self):
        return 'frequently_entry_detail'

    def get_view_kwargs(self):
        return {'pk': self.entry.pk, 'slug': self.entry.slug}

    def test_view(self):
        self.should_be_callable_when_anonymous()


class EntryCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the ``EntryCreateView`` generic view class."""
    def setUp(self):
        self.user = UserFactory()

    def get_view_name(self):
        return 'frequently_submit_question'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.user)
        data = {
            'question': 'Foo',
        }
        resp = self.client.post(self.get_url(), data=data)
        self.assertRedirects(
            resp,
            reverse('frequently_category_list'),
            msg_prefix=('Should redirect to category list view.')
        )
