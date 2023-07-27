from django import template
from datetime import date


register = template.Library()

@register.filter
def calcular_idade(data_anv):
    if data_anv is None:
        return ''

    hoje = date.today()
    idade = hoje.year - data_anv.year
    if hoje.month < data_anv.month or (hoje.month == data_anv.month and hoje.day < data_anv.day):
        idade -= 1
    return idade