"""
URLs for the ``django-frequently`` application.

"""
from django.conf.urls.defaults import patterns, url

from frequently.views import (
    EntryCreateView,
    EntryDetailView,
    EntryCategoryDetailView,
    EntryCategoryListView,
)


urlpatterns = patterns('',
    url(r'^$',
        EntryCategoryListView.as_view(),
        name='category_list',
    ),

    url(r'^(?P<pk>\d+)/(?P<slug>[a-z-0-9]+)/$',
        EntryCategoryDetailView.as_view(),
        name='category_detail',
    ),

    url(r'^question/(?P<pk>\d+)/(?P<slug>[a-z-0-9]+)/$',
        EntryDetailView.as_view(),
        name='entry_detail',
    ),

    url(r'^your-question/$',
        EntryCreateView.as_view(),
        name='submit_question',
    ),
)
