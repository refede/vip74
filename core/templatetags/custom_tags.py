from django import template

register = template.Library()

@register.filter(name='to_percentage')
def to_percentage(value):
    """
    Convierte un valor decimal en un porcentaje.
    Por ejemplo, 0.10 se convierte en 10%.
    """
    try:
        value_as_float = float(value)
        return f'{value_as_float * 100:.0f}%'  # Multiplicamos por 100 y le añadimos el símbolo %
    except (ValueError, TypeError):
        return ''


@register.filter(name='por_cien')
def por_cien(value):
    try:
        value_as_float = float(value)
        return f'{value_as_float * 100:.0f}'
    except (ValueError, TypeError):
        return ''


@register.filter(name='reemplazar_zero')
def reemplazar_zero(value, texto_alternativo):
    if value == 0:
        return texto_alternativo
    return value
