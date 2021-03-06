from django import template
from django.conf import settings

register = template.Library()

# settings value
@register.simple_tag
def includesettings(name):
    return getattr(settings, name, "")
