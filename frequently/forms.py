"""
Forms for the ``django-frequently`` application.

"""
from django import forms

from frequently.models import Entry


class EntryForm(forms.ModelForm):
    """
    Form to submit a new entry.

    """
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
            'votes',
            'published',
        )

    def __init__(self, owner=False, *args, **kwargs):
        self.owner = owner
        super(EntryForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.owner:
            self.instance.owner = self.owner
        return super(EntryForm, self).save(*args, **kwargs)
