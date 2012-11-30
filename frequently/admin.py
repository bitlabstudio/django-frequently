"""Admin sites for the ``django-frequently`` app."""
from django.contrib import admin

from frequently import models


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('entry', 'user_email', 'submission_date', 'validation')

    def user_email(self, obj):
        if obj.user and obj.user.email:
            return "{0}".format(obj.user.email)
        return ""
    user_email.short_description = 'Email'


admin.site.register(models.Entry)
admin.site.register(models.EntryCategory)
admin.site.register(models.Feedback, FeedbackAdmin)
