"""NavBar models for building and managing dynamic site navigation
"""
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from categories.base import CategoryBase

from navbar.settings import STORAGE_CLASS, UPLOAD_TO

USER_TYPE_CHOICES = [
    ('E', _('Everybody')),
    ('A', _('Anonymous Only')),
    ('L', _('Logged In')),
    ('S', _('Staff')),
    ('X', _('Superuser')),
]

SELECTION_TYPE_CHOICES = [
    ('N', _('Never')),
    ('E', _('Exact')),
    ('P', _('ExactOrParent')),
    ('A', _('OnPathOrParent (default)'))
]


class NavBarRootManager(models.Manager):
    def get_query_set(self):
        qset = super(NavBarRootManager, self).get_query_set()
        return qset.filter(parent__isnull=True)


class NavBarEntry(CategoryBase):
    title = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("mouse hover description"))
    url = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    ## advanced permissions
    path_type = models.CharField(_('path match type'),
        max_length=1,
        choices=SELECTION_TYPE_CHOICES,
        default='A',
        help_text=_("Control how this element is marked 'selected' based on the "
                 "request path."))
    user_type = models.CharField(_('user login type'),
        max_length=1,
        choices=USER_TYPE_CHOICES,
        default=USER_TYPE_CHOICES[0][0])
    groups = models.ManyToManyField(Group, null=True, blank=True)

    ## advance style options
    cssclass = models.CharField(_("Normal CSS Class"),
        blank=True,
        max_length=100,)
    active_cssclass = models.CharField(_("Active CSS Class"),
        blank=True,
        max_length=100, )
    img = models.FileField(_("Menu Image"),
        blank=True, null=True,
        upload_to=UPLOAD_TO,
        storage=STORAGE_CLASS())

    objects = models.Manager()
    top = NavBarRootManager()

    class Meta:
        verbose_name = 'navigation bar element'
        verbose_name_plural = 'navigation bar elements'
        ordering = ('tree_id', 'order',)

    def __unicode__(self):
        return self.name

    def save(self):
        cache.delete('site_navtree')
        cache.delete('site_navtree_super')
        return super(NavBarEntry, self).save()

    def delete(self, *args, **kwdargs):
        cache.delete('site_navtree')
        cache.delete('site_navtree_super')
        return super(NavBarEntry, self).delete(*args, **kwdargs)
