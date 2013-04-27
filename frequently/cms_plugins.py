"""CMS Plugins for the ``frequently`` app."""
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import EntryCategoryPlugin


class CMSFrequentlyCategoryPlugin(CMSPluginBase):
    name = _('Frequently Asked Questions (Categories)')
    model = EntryCategoryPlugin
    render_template = 'frequently/plugin.html'

    def render(self, context, instance, placeholder):
        context.update({
            'categories': instance.categories.all(),
        })
        return context

plugin_pool.register_plugin(CMSFrequentlyCategoryPlugin)
