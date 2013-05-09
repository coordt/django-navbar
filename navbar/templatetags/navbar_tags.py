from django.template import Library
from django import template
from django.conf import settings
from navbar.models import NavBarEntry


def _getdefault(name, default=None):
    try:
        default = getattr(settings, name)
    except:
        pass
    return default

SHOW_DEPTH = _getdefault('NAVBAR_TREE_SHOW_DEPTH', -1)

numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
           'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen',
           'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eightteen',
           'nineteen', ]

_dig = numbers[1:10]
for ent in ['twenty', 'thirty', 'fourty', 'fifty', 'sixty', 'seventy',
            'eighty', 'ninety']:
    numbers.append(ent)
    numbers.extend(ent + "-" + num for num in _dig)

register = Library()


@register.filter
def cssnumber(num):
    """
    Like humanize appnum but goes the full gambit from 0 to 99.
    Is not translated as this is intended for CSS use.
    0 : zero
    10: ten
    45: fourty-five

    use the filter tag if you want a translation...
    """
    return numbers[num]


@register.inclusion_tag('navbar/subtree.html')
def subtree(children, depth=0):
    """
    Process a sub part of the nav tree
    """
    return {
        'subtree': children,
        'depth': depth + 1,
        'show_unselected': (SHOW_DEPTH == -1 or depth < SHOW_DEPTH),
        'level': numbers[depth + 1]
    }


@register.inclusion_tag('navbar/tree.html', takes_context=True)
def navtree(context):
    """
    Simpler helper so you dont need to do the include ;-)
    """
    return context


@register.inclusion_tag('navbar/navbar.html', takes_context=True)
def navbar(context):
    """
    Simpler helper so you dont need to do the include ;-)
    """
    return context


@register.inclusion_tag('navbar/navbars.html', takes_context=True)
def navbars(context):
    """
    Simpler helper so you dont need to do the include ;-)
    """
    return context


def resolve_or_val(variable, context):
    try:
        return variable.resolve(context)
    except template.VariableDoesNotExist:
        return variable.var


class NavBarNode(template.Node):
    """
    Render a specific navbar
    """
    def __init__(self, navbar_name, template_name='navbar/navbar.html'):
        self.navbar_name = template.Variable(navbar_name)
        self.template_name = template.Variable(template_name)

    def render(self, context):
        from django.template.loader import render_to_string
        navbar_name = resolve_or_val(self.navbar_name, context)
        try:
            navbar = NavBarEntry.objects.get(name=navbar_name)
        except NavBarEntry.DoesNotExist:
            if settings.TEMPLATE_DEBUG:
                return 'Cant Find %s' % navbar_name
            else:
                return ''
        template_name = resolve_or_val(self.template_name, context)
        return render_to_string(
            template_name,
            {'navbar': navbar.children.all()},
            context)


def render_navbar(parser, token):
    """
    render a specific navbar

    {% render_navbar navbar_name [templatename.html]}
    """
    bits = token.split_contents()
    navbar_name = ''
    template_name = 'navbar/navbar.html'
    if len(bits) == 3:
        navbar_name = bits[1]
        template_name = bits[2]
    elif len(bits) == 2:
        navbar_name = bits[1]
    else:
        raise template.TemplateSyntaxError(
            "%r tag requires a navbar name." % token.contents.split()[0])
    return NavBarNode(navbar_name, template_name)

register.tag(render_navbar)


class TopNavBarNode(template.Node):
    """
    Render a specific navbar
    """
    def __init__(self, template_name='navbar/navbar.html'):
        self.template_name = template.Variable(template_name)

    def render(self, context):
        from django.template.loader import render_to_string
        try:
            navbar = NavBarEntry.objects.filter(parent__isnull=True)
        except NavBarEntry.DoesNotExist:
            if settings.TEMPLATE_DEBUG:
                return 'Cant Find Top navbar items'
            else:
                return ''
        template_name = resolve_or_val(self.template_name, context)
        return render_to_string(
            template_name,
            {'navbar': navbar},
            context)


def render_topnavbar(parser, token):
    """
    render a specific navbar

    {% render_navbar navbar_name [templatename.html]}
    """
    bits = token.split_contents()
    template_name = 'navbar/navbar.html'
    if len(bits) == 2:
        template_name = bits[1]
    return TopNavBarNode(template_name)

register.tag(render_topnavbar)
