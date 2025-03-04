from django import template

register = template.Library()

@register.filter
def widget_type(field):
    """Returns the widget type for a given form field."""
    return field.field.widget.__class__.__name__


@register.filter
def choices(field):
    """Returns the widget type for a given form field."""
    return field.field._choices