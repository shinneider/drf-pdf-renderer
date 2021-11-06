from datetime import datetime

from django import template
from django.template.defaultfilters import date as date_filter


register = template.Library()


@register.filter
def isodate(value, arg):
    return date_filter(datetime.strptime(value, "%Y-%m-%d").date(), arg) if value else ''


@register.filter
def format_cpf(value):
    return "{}{}{}.{}{}{}.{}{}{}-{}{}".format(*value) if len(value) == 11 else value


@register.filter(name='lookup')
def lookup(dictionary, key):
    return dictionary.get(key)
