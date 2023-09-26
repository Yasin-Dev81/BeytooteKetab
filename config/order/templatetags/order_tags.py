from django import template

register = template.Library()


@register.filter
def discount_kart(value):
    return round(0.75 * value)
