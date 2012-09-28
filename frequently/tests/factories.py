"""
Factories for the ``django-frequently`` app.

"""
import factory

from frequently.models import Example


class ExampleFactory(factory.Factory):
    FACTORY_FOR = Example

    text = 'Foobar'
