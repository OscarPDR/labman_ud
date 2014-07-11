# -*- encoding: utf-8 -*-


from django import template

from inflection import underscore

register = template.Library()


@register.filter(name='sanitize')
def sanitize(value):
    return underscore(value).replace('_', ' ').capitalize()
