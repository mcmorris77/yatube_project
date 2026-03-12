from django import template

register = template.Library()


@register.filter
def addclass(field, css_class):
    """Добавляет CSS класс к полю формы."""
    return field.as_widget(attrs={"class": css_class})