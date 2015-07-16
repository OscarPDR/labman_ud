# -*- encoding: utf-8 -*-

from django import template

from entities.utils.models import PersonRelatedToAward

register = template.Library()


@register.simple_tag
def awardee_names(award_instance):

    awardees = PersonRelatedToAward.objects.filter(award=award_instance).order_by('person__full_name').values_list('person__full_name', flat=True)
    return ', '.join(awardees)
