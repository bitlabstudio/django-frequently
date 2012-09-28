"""URLs for the ``django-frequently`` application."""
from django.conf.urls.defaults import patterns, url

from frequently.views import HomeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
)
