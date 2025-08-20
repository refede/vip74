from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_item_from_dict(dictionary, key):
    return dictionary.get(key)


# Filtro para obtener la primera parte de una cadena separada por un delimitador
@register.filter
def split_first(value, delimiter="+"):
    return value.split(delimiter)[0]


# Filtro para obtener la segunda parte de una cadena separada por un delimitador
@register.filter
def split_last(value, delimiter="+"):
    return value.split(delimiter)[1]


@register.filter
def split_by_dash(value):
    """Divide una cadena separada por guiones en una lista de sus componentes."""
    return value.split("+")
