"""
Factories for the ``django-frequently`` app.

"""
import factory

from django.utils import timezone

from frequently import models
from django_libs.tests.factories import UserFactory


class EntryCategoryFactory(factory.Factory):
    FACTORY_FOR = models.EntryCategory

    name = factory.Sequence(lambda n: 'Entry Category {0}'.format(n))
    slug = factory.Sequence(lambda n: 'entry-category-{0}'.format(n))


class EntryFactory(factory.Factory):
    FACTORY_FOR = models.Entry

    owner = factory.SubFactory(UserFactory)
    question = factory.Sequence(lambda n: 'Question {0}'.format(n))
    slug = factory.Sequence(lambda n: 'question-{0}'.format(n))
    creation_date = timezone.now()
    last_view_date = timezone.now()
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

    submission_date = timezone.now()
    validation = 'P'


class EntryCategoryPluginFactory(factory.Factory):
    """Base factory for factories for ``EntryCategoryPlugin`` models."""
    FACTORY_FOR = models.EntryCategoryPlugin
