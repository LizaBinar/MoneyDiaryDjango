from django import template
from unicodedata import decimal

register = template.Library()


@register.filter
def money_filter(value):
    value = float(value)
    minus = ''
    if value < 0:
        minus = '-'
        value = -value
    value = str(value)
    if value[-2] == ".":
        value = value + '0'
    lenght = len(value)
    carry_space = 6
    while carry_space < lenght:
        value = value[:-carry_space] + ' ' + value[-carry_space:]
        carry_space += 4
        lenght = len(value)
    # value = value[:-2] + ',' + value[-2:]
    value = minus + value
    return value


@register.filter
def year_month_day(value):
    return "%d-%d-%d" % (value.year, value.month, value.day)