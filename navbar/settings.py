from django.conf import settings
from django.core.files.storage import get_storage_class

STATIC_URL = getattr(settings, 'STATIC_URL', settings.MEDIA_URL)

DEFAULT_SETTINGS = {
    'MEDIA_PATH': '%snavbar/' % STATIC_URL,
    'TREE_INITIAL_STATE': 'collapsed',
    'STORAGE_CLASS': settings.DEFAULT_FILE_STORAGE,
    'UPLOAD_TO': 'navbar',
    'MAX_DEPTH': -1,
    'MARK_SELECTED': True,
    'SHOW_DEPTH': -1,
    'CRUMBS_STRIP_ROOT': True,
    'CRUMBS_HOME': 'home',
    'ROOT_URL': '/',
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()

USER_SETTINGS.update(getattr(settings, 'NAVBAR_SETTINGS', {}))

USER_SETTINGS['STORAGE_CLASS'] = get_storage_class(USER_SETTINGS['STORAGE_CLASS'])

globals().update(USER_SETTINGS)
