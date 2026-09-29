from django import template

register = template.Library()


@register.filter
def splitlines_clean(value):
    return [line.strip() for line in (value or '').splitlines() if line.strip()]
