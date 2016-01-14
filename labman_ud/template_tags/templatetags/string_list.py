# -*- encoding: utf-8 -*-

import json

from django.template import Library

register = Library()

### string_list
####################################################################################################

@register.filter
def string_list( objectList ):
	return json.dumps(list(objectList))