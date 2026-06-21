from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def money(value):
    if value is None:
        return ""

    value = int(value)
    return f"{intcomma(value).replace(',', '.')} ₫"
