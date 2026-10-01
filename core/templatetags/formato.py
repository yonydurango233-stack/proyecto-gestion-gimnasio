from django import template

register = template.Library()

@register.filter
def moneda(value):
    try:
        value = int(float(value))
    except (ValueError, TypeError):
        return value
    return f"{value:,}".replace(",", ".")