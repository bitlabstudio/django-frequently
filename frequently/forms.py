"""
Forms for the ``django-frequently`` application.

"""
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from frequently.models import Entry


class EntryForm(forms.ModelForm):
    """
    Form to submit a new entry.

    """
    name = forms.CharField(max_length=100, label=_('Your Name'))
    email = forms.EmailField()

    class Meta:
        model = Entry
        exclude = (
            'owner',
            'slug',
            'answer',
            'category',
            'creation_date',
            'last_view_date',
            'amount_of_views',
            'upvotes',
            'downvotes',
            'published',
            'fixed_position',
        )

    def __init__(self, owner=None, *args, **kwargs):
        self.owner = owner
        super(EntryForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.owner:
            self.instance.owner = self.owner
        try:
            settings.FREQUENTLY_RECIPIENTS
            ctx_dict = {
                'name': self.cleaned_data['name'],
                'email': self.cleaned_data['email'],
                'question': self.cleaned_data['question'],
            }
            subject = render_to_string(
                    'frequently/email/new_question_subject.txt',
                    ctx_dict)
            subject = ''.join(subject.splitlines())
            message = render_to_string(
                    'frequently/email/new_question_body.txt',
                    ctx_dict)
            to = [item[1] for item in settings.FREQUENTLY_RECIPIENTS]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)
        except AttributeError:
            pass
        return super(EntryForm, self).save(*args, **kwargs)
