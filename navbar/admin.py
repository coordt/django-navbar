from django.contrib import admin
from django import forms
from navbar.models import NavBarEntry
import re
from tree_editor import TreeEditor

url_re = re.compile(r'^(https?://([a-zA-Z0-9]+\.)+[a-zA-Z0-9]+([:@][a-zA-Z0-9@%-_\.]){0,2})?/\S*$')

class NavBarEntryAdminForm(forms.ModelForm):
    class Meta:
        model = NavBarEntry

    def clean_url(self):
        url = self.cleaned_data["url"].strip()
        if not url_re.search(url):
            raise forms.ValidationError("A valid URL is required.")
        return url
        
    def clean_parent(self):
        parent = self.cleaned_data["parent"]
        try:
            pids = []
            while parent:
                parent = NavBarEntry.objects.get(pk=parent.id)
                if parent.id in pids:
                    raise forms.ValidationError(
                        u"Creates a cyclical reference.")
                elif parent.parent != None:
                    parent = parent.parent
                else: break
                pids.append(parent.id)
        except NavBarEntry.DoesNotExist:
            raise forms.ValidationError(u"Could not find parent id.")
        return parent

class NavBarEntryAdmin(TreeEditor, admin.ModelAdmin):
    form = NavBarEntryAdminForm
    fieldsets = (
        (None, {'fields': ('name', 'title', 'url', 'order',)}),
        ('Advanced Permissions', {
            'classes': ('collapse',),
            'fields': ('path_type', 'user_type', 'groups', )}),
        ('Style Options', {
            'classes': ('collapse',),
            'fields': ('cssclass', 'active_cssclass', 'img')
        })
    )
    list_display = ('name', 'url', 'order', )
    search_fields = ('url', 'name', 'title')
    filter_horizontal = ("groups",)

admin.site.register(NavBarEntry, NavBarEntryAdmin)
