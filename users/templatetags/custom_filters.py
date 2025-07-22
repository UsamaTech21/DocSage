from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """Add a CSS class to form fields."""
    return field.as_widget(attrs={"class": css})
