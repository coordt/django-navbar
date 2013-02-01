import re

from django.contrib import admin
from django import forms

from navbar.models import NavBarEntry
from categories.base import CategoryBaseAdmin

url_re = re.compile(r'^(https?://([a-zA-Z0-9]+\.)+[a-zA-Z0-9]+([:@][a-zA-Z0-9@%-_\.]){0,2})?/\S*$')


class NavBarEntryAdmin(CategoryBaseAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'title', 'url', 'order', 'parent', 'active')}),
        ('Advanced Permissions', {
            'classes': ('collapse',),
            'fields': ('path_type', 'user_type', 'groups', 'slug')}),
        ('Style Options', {
            'classes': ('collapse',),
            'fields': ('cssclass', 'active_cssclass', 'img')
        })
    )
    list_display = ('name', 'url', 'order', )
    search_fields = ('url', 'name', 'title')
    filter_horizontal = ("groups",)

admin.site.register(NavBarEntry, NavBarEntryAdmin)
