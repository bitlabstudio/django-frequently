"""
Factories for the ``django-frequently`` app.

"""
import factory

from django.utils import timezone

from frequently import models
from django_libs.tests.factories import UserFactory


class EntryCategoryFactory(factory.Factory):
    FACTORY_FOR = models.EntryCategory

    name = "Entry category"


class EntryFactory(factory.Factory):
    FACTORY_FOR = models.Entry

    owner = factory.SubFactory(UserFactory)
    question = 'How can I stop using your awesome app?'
    creation_date = timezone.datetime.now()
    last_view_date = timezone.datetime.now()
    published = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        item = super(EntryFactory, cls)._prepare(
            create, **kwargs)
        if create:
            item.category.add(EntryCategoryFactory())
        return item


class FeedbackFactory(factory.Factory):
    FACTORY_FOR = models.Feedback

    submission_date = timezone.datetime.now()
    validation = 'P'
