from django.conf import settings
import django

DJANGO10_COMPAT = django.VERSION[0] < 1 or (django.VERSION[0] == 1 and django.VERSION[1] < 1)
STATIC_URL = getattr(settings, 'STATIC_URL', settings.MEDIA_URL)

DEFAULT_SETTINGS = {
    'MEDIA_PATH': '%snavbar/' % STATIC_URL,
    'TREE_INITIAL_STATE': 'collapsed',
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()

USER_SETTINGS.update(getattr(settings, 'NAVBAR_SETTINGS', {}))

globals().update(USER_SETTINGS)