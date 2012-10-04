"""
Views for the ``django-frequently`` application.

"""
from math import fsum

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView

from frequently.forms import EntryForm
from frequently.models import Entry, EntryCategory, Feedback


class FeedbackMixin(object):
    """
    Mixin to handle positive and negative feedback requests.

    """
    def get_context_data(self, **kwargs):
        context = super(FeedbackMixin, self).get_context_data(**kwargs)
        for key in self.request.GET.keys():
            if key.startswith('down'):
                context.update({'depreciate': int(key.replace('down', ''))})
                return context
        return context

    def post(self, request, *args, **kwargs):
        feedback = Feedback()
        if request.user.is_authenticated():
            feedback.user = request.user
        for key in self.request.POST.keys():
            if key.startswith('up'):
                entry = Entry.objects.get(pk=key.replace('up', ''))
                entry.votes += 1
                feedback.entry = entry
                feedback.validation = "P"
                entry.save()
                feedback.save()
                break
            elif key.startswith('down'):
                entry = Entry.objects.get(pk=key.replace('down', ''))
                entry.votes -= 1
                feedback.entry = entry
                feedback.validation = "N"
                feedback.remark = request.POST.get("remark")
                entry.save()
                feedback.save()
                break
        return self.get(self, request, *args, **kwargs)


class EntryCategoryListView(FeedbackMixin, ListView):
    """
    Main view to display all categories and their entries.

    """
    model = EntryCategory
    template_name = "frequently/entrycategory_list.html"

    def get_queryset(self):
        """
        Custom ordering. First we get the average views and votes for
        the categories's entries. Second we created a rank by multiplying
        both. Last, we sort categories by this rank from top to bottom.

        Example:
        - Cat_1
            - Entry_1 (500 Views, Vote status 2)
            - Entry_2 (200 Views, Vote status -4)
            - Entry_3 (100 Views, Vote status 3)
        - Cat_2
            - Entry_1 (200 Views, Vote status 7)
            - Entry_2 (50 Views, Vote status 2)

        Result:
        Cat_1 has a rank by: 88.88 (average views: 266.66, average votes: 0.33)
        Cat_2 has a rank by: 562.5 (average views: 125, average votes: 4.5)

        Cat_2 will be displayed at the top. The algorithm is quality-oriented,
        as you can see.

        """
        self.queryset = super(EntryCategoryListView, self).get_queryset()
        if self.queryset:
            for category in self.queryset:
                entries = category.get_entries()
                if entries:
                    amount_list = [e.amount_of_views for e in entries]
                    votes_list = [e.votes for e in entries]
                    views_per_entry = fsum(amount_list) / len(amount_list)
                    votes_per_entry = fsum(votes_list) / len(votes_list)
                    category.last_rank = views_per_entry * votes_per_entry
                    category.save()
                else:
                    self.queryset = self.queryset.exclude(pk=category.pk)
            self.queryset = sorted(self.queryset, key=lambda c: c.last_rank,
                                   reverse=True)
        return self.queryset


class EntryCategoryDetailView(FeedbackMixin, DetailView):
    """
    Main view to display one category and its entries.

    """
    model = EntryCategory


class EntryDetailView(FeedbackMixin, DetailView):
    """
    Main view to display one entry.

    """
    model = Entry

    def get_object(self, **kwargs):
        obj = super(EntryDetailView, self).get_object(**kwargs)
        obj.last_view_date = timezone.datetime.now()
        obj.save()
        return obj


class EntryCreateView(CreateView):
    """
    Feedback submission form view.

    """
    model = Entry
    form_class = EntryForm

    def get_form_kwargs(self):
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        if self.request.user.is_authenticated():
            kwargs.update({
                'owner': self.request.user,
            })
        return kwargs

    def get_success_url(self):
        return reverse('frequently:category_list')
