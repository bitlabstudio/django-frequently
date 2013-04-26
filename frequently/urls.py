"""
URLs for the ``django-frequently`` application.

"""
from django.conf.urls.defaults import patterns, url

from frequently.views import (
    EntryCategoryListView,
    EntryCreateView,
    EntryDetailView,
)


urlpatterns = patterns(
    '',
    url(r'^$',
        EntryCategoryListView.as_view(),
        name='frequently_list'),

    url(r'^your-question/$',
        EntryCreateView.as_view(),
        name='frequently_submit_question'),

    url(r'^(?P<slug>[a-z-0-9]+)/$',
        EntryDetailView.as_view(),
        name='frequently_entry_detail'),
)
