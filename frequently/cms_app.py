"""
django-cms Apphook for the ``django-frequently`` application.

"""
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class BlogApphook(CMSApp):
    name = _("Frequently App")
    urls = ["frequently.urls"]

apphook_pool.register(BlogApphook)
