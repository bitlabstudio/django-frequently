"""Admin sites for the ``django-frequently`` app."""
from django.contrib import admin

from frequently import models


admin.site.register(models.Entry)
admin.site.register(models.EntryCategory)
admin.site.register(models.Feedback)
