
from django import template
from random import randint

register = template.Library()


###     randInt
####################################################################################################

@register.simple_tag
def randInt(min, max):
    return randint(min, max)
