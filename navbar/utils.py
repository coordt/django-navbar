
def _Qperm(user=None):
    from django.db.models.query import Q
    exQ = Q()
    if user is None or user.is_anonymous():
        exQ = (Q(user_type__exact = 'A') | Q(user_type__exact = 'E')) & Q(
            groups__isnull=True)
    elif user.is_superuser:
        exQ = ~Q(user_type__exact = 'A')
    elif user.is_staff:
        exQ = (Q(user_type__exact = 'E') | Q(user_type__exact = 'L') |
               Q(user_type__exact = 'S')) & (
                    Q(groups__in=user.groups.all()) | Q(groups__isnull=True))
    else:
        exQ = (Q(user_type__exact = 'E') | Q(user_type__exact = 'L')) & (
                    Q(groups__in=user.groups.all()) | Q(groups__isnull=True))
    return exQ

def generate_navtree(user=None, maxdepth=-1):
    from models import NavBarEntry
    if maxdepth == 0: return [] ## silly...
    permQ = _Qperm(user)
    urls = {}
    def navent(ent, invdepth, parent):
        current = {'name': ent.name, 'title': ent.title, 'url': ent.url,
                   'selected': False, 'path_type': ent.path_type, 'parent': parent}
        urls.setdefault(ent.url, current)
        current['children'] = navlevel(ent.children, invdepth-1, current)
        return current
    def navlevel(base, invdepth, parent=None):
        if invdepth == 0 : return []
        return [ navent(ent, invdepth, parent)
                        for ent in base.filter(permQ).distinct() ]
    tree = navlevel(NavBarEntry.top, maxdepth)
    urls = sorted(urls.iteritems(), key=lambda x: x[0], reverse=True)
    return {'tree': tree, 'byurl': urls}

def get_navtree(user=None, maxdepth=-1):
    import models
    cachename = 'site_navtree'
    timeout = 60*60*24
    if user is not None and not user.is_anonymous():
        if user.is_superuser:
            cachename = 'site_navtree_super'
        else:
            cachename = 'site_navtree_' + str(user.id)
            timeout = 60*15
    data = models.cache.get(cachename)
    if data is None:
        data = generate_navtree(user, maxdepth)
        models.cache.set(cachename, data, timeout)
    return data

def get_navbar(user=None):
    from models import NavBarEntry
    return NavBarEntry.top.filter(_Qperm(user))


"""
Provides compatibility with Django 1.1

Copied from django.contrib.admin.util
"""
from django.db import models
from django.utils.encoding import force_unicode, smart_unicode, smart_str

def lookup_field(name, obj, model_admin=None):
    opts = obj._meta
    try:
        f = opts.get_field(name)
    except models.FieldDoesNotExist:
        # For non-field values, the value is either a method, property or
        # returned via a callable.
        if callable(name):
            attr = name
            value = attr(obj)
        elif (model_admin is not None and hasattr(model_admin, name) and
          not name == '__str__' and not name == '__unicode__'):
            attr = getattr(model_admin, name)
            value = attr(obj)
        else:
            attr = getattr(obj, name)
            if callable(attr):
                value = attr()
            else:
                value = attr
        f = None
    else:
        attr = None
        value = getattr(obj, name)
    return f, attr, value


def label_for_field(name, model, model_admin=None, return_attr=False):
    """
    Returns a sensible label for a field name. The name can be a callable or the
    name of an object attributes, as well as a genuine fields. If return_attr is
    True, the resolved attribute (which could be a callable) is also returned.
    This will be None if (and only if) the name refers to a field.
    """
    attr = None
    try:
        field = model._meta.get_field_by_name(name)[0]
        if isinstance(field, RelatedObject):
            label = field.opts.verbose_name
        else:
            label = field.verbose_name
    except models.FieldDoesNotExist:
        if name == "__unicode__":
            label = force_unicode(model._meta.verbose_name)
            attr = unicode
        elif name == "__str__":
            label = smart_str(model._meta.verbose_name)
            attr = str
        else:
            if callable(name):
                attr = name
            elif model_admin is not None and hasattr(model_admin, name):
                attr = getattr(model_admin, name)
            elif hasattr(model, name):
                attr = getattr(model, name)
            else:
                message = "Unable to lookup '%s' on %s" % (name, model._meta.object_name)
                if model_admin:
                    message += " or %s" % (model_admin.__class__.__name__,)
                raise AttributeError(message)

            if hasattr(attr, "short_description"):
                label = attr.short_description
            elif callable(attr):
                if attr.__name__ == "<lambda>":
                    label = "--"
                else:
                    label = pretty_name(attr.__name__)
            else:
                label = pretty_name(name)
    if return_attr:
        return (label, attr)
    else:
        return label

def display_for_field(value, field):
    from django.contrib.admin.templatetags.admin_list import _boolean_icon
    from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
    
    if field.flatchoices:
        return dict(field.flatchoices).get(value, EMPTY_CHANGELIST_VALUE)
    # NullBooleanField needs special-case null-handling, so it comes
    # before the general null test.
    elif isinstance(field, models.BooleanField) or isinstance(field, models.NullBooleanField):
        return _boolean_icon(value)
    elif value is None:
        return EMPTY_CHANGELIST_VALUE
    elif isinstance(field, models.DateField) or isinstance(field, models.TimeField):
        return formats.localize(value)
    elif isinstance(field, models.DecimalField):
        return formats.number_format(value, field.decimal_places)
    elif isinstance(field, models.FloatField):
        return formats.number_format(value)
    else:
        return smart_unicode(value)
