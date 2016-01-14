# -*- coding: utf-8 -*-

from django.template import Library

register = Library()

###     get_range
####################################################################################################

@register.filter
def get_range( value ):
    return range( 1, int(value) + 1 )