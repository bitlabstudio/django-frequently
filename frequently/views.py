"""
Views for the ``django-frequently`` application.

"""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'frequently/home.html'

    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
