import re

from django import template
from django.utils.text import normalize_newlines
from django.utils.safestring import mark_safe, SafeData
from django.utils.html import escape

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=True)
def greentext(value, autoescape=None):
    autoescape = autoescape and not isinstance(value, SafeData)
    value = normalize_newlines(value)
    if autoescape:
        value = escape(value)
    # Split up the text into lines because we want to apply the filter
    # on a per-line basis
    values = value.split("\n")
    new_values = []
    # For each string, find first single > symbol and add the span
    for string in values:
        string = re.sub(r'(&gt;.*$)',
                        r'<span class="quote">\1</span>',
                        string)
        new_values.append(string)
    new_value = "\n".join(new_values)
    return mark_safe(new_value)

@register.filter(is_safe=True, needs_autoescape=True)
def cut_long_comment(value, autoescape=None):
    value = normalize_newlines(value)
    values = value.split("\n")
    if len(values) > 16:
        values = values[:16]
    new_value = "\n".join(values)
    return new_value

@register.filter
def will_cut_long_comment(value):
    value = normalize_newlines(value)
    values = value.split("\n")
    return len(values) > 16
