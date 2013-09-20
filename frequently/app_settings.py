"""Default values for settings of the frequently app."""
from django.conf import settings


REQUIRE_EMAIL = getattr(settings, 'FREQUENTLY_REQUIRE_EMAIL', True)
