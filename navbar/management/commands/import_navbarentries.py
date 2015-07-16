from categories.management.commands.import_categories import Command as CategoriesCommand
from slugify import slugify

from navbar.models import NavBarEntry
from categories.settings import SLUG_TRANSLITERATOR


class Command(CategoriesCommand):
    help = "Imports nav bar entry tree(s) from a file. Sub entries must be indented by the same multiple of spaces or tabs."
    args = "file_path [file_path ...]"

    def make_category(self, string, parent=None, order=1):
        """
        Make and save a category object from a string
        """
        slug = slugify(SLUG_TRANSLITERATOR(string.strip()))[:49]
        if parent:
            parent_url = parent.url.rstrip("/")
        else:
            parent_url = ""

        cat = NavBarEntry(
            name=string.strip(),
            slug=slug,
            url="%s/%s/" % (parent_url, slug),
            order=order
        )
        cat._tree_manager.insert_node(cat, parent, 'last-child', True)
        cat.save()
        if parent:
            parent.rght = cat.rght + 1
            parent.save()
        return cat
