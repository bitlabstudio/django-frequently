"""
Views for the ``django-frequently`` application.

"""
from math import fsum

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse
from django.template.response import TemplateResponse
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
        context.update({'rated_entries': self.request.session.get(
            'rated_entries', False)})
        for key in self.request.POST.keys():
            if key.startswith('down') or key.startswith('up'):
                context.update({
                    'feedback_entry': int(
                        key.replace('up', '').replace('down', '')),
                    'feedback': self.feedback,
                })
                return context
        return context

    def post(self, request, *args, **kwargs):
        self.feedback = Feedback()
        for key in request.POST.keys():
            if key == "refresh_last_view":
                entry = Entry.objects.get(
                    pk=request.POST['refresh_last_view'])
                entry.last_view_date = timezone.now()
                entry.save()
                return HttpResponse(entry.last_view_date)
            if key == "user_id":
                try:
                    user_id = int(request.POST.get('user_id'))
                    self.feedback.user = User.objects.get(pk=user_id)
                except ValueError:
                    pass
            if key.startswith('up') or key.startswith('down'):
                entry = Entry.objects.get(
                    pk=key.replace('up', '').replace('down', ''))
                if not request.session.get('rated_entries', False):
                    request.session['rated_entries'] = []
                if not entry.pk in request.session['rated_entries']:
                    request.session['rated_entries'].append(entry.pk)
                    request.session.modified = True
                    self.feedback.entry = entry
                    if key.startswith('up'):
                        entry.upvotes += 1
                        self.feedback.validation = "P"
                    if key.startswith('down'):
                        entry.downvotes += 1
                        self.feedback.validation = "N"
                    entry.save()
                    self.feedback.save()
                    if request.is_ajax():
                        return TemplateResponse(
                            request,
                            'frequently/partials/feedback_form.html',
                            {
                                'feedback_entry': entry.pk,
                                'feedback': self.feedback,
                            }
                        )
            elif key == 'ratingID' and request.is_ajax():
                entry = Entry.objects.get(
                    pk=request.POST.get('ratingID').replace('ratingID', ''))
                return HttpResponse(entry.rating())
            elif key.startswith('feedback'):
                self.feedback = Feedback.objects.get(
                    pk=key.replace('feedback', ''))
                self.feedback.remark = request.POST.get("remark")
                self.feedback.save()
                if request.is_ajax():
                    return TemplateResponse(
                        request,
                        'frequently/partials/feedback_form.html',
                        {
                            'feedback_send': True,
                        }
                    )
        return self.get(self, request, *args, **kwargs)


class EntryCategoryListView(FeedbackMixin, ListView):
    """
    Main view to display all categories and their entries.

    """
    model = EntryCategory
    template_name = "frequently/entrycategory_list.html"

    def get_queryset(self):
        """
        Custom ordering. First we get the average views and rating for
        the categories's entries. Second we created a rank by multiplying
        both. Last, we sort categories by this rank from top to bottom.

        Example:
        - Cat_1
            - Entry_1 (500 Views, Rating 2)
            - Entry_2 (200 Views, Rating -4)
            - Entry_3 (100 Views, Rating 3)
        - Cat_2
            - Entry_1 (200 Views, Rating 7)
            - Entry_2 (50 Views, Rating 2)

        Result:
        Cat_1 has a rank by: 88.88 (avg. views: 266.66, avg. rating: 0.33)
        Cat_2 has a rank by: 562.5 (avg. views: 125, avg. rating: 4.5)

        Cat_2 will be displayed at the top. The algorithm is quality-oriented,
        as you can see.

        """
        self.queryset = super(EntryCategoryListView, self).get_queryset()
        if self.queryset:
            for category in self.queryset:
                entries = category.get_entries()
                if entries:
                    amount_list = [e.amount_of_views for e in entries]
                    rating_list = [e.rating() for e in entries]
                    views_per_entry = fsum(amount_list) / len(amount_list)
                    rating_per_entry = fsum(rating_list) / len(rating_list)
                    category.last_rank = views_per_entry * rating_per_entry
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
        obj.last_view_date = timezone.now()
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
        return reverse('frequently_category_list')
