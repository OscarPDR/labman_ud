# -*- encoding: utf-8 -*-

from django import forms

from entities.persons.models import Person

from entities.utils.models import GeographicalScope


# Create your forms here.


PROJECT_STATUS = (
    ('Any', 'Any'),
    ('Not started', 'Not started'),
    ('In development', 'In development'),
    ('Finished', 'Finished'),
)

YEARS = (
    ('2004', '2004'),
    ('2005', '2005'),
    ('2006', '2006'),
    ('2007', '2007'),
    ('2008', '2008'),
    ('2009', '2009'),
    ('2010', '2010'),
    ('2011', '2011'),
    ('2012', '2012'),
    ('2013', '2013'),
    ('2014', '2014'),
    ('2015', '2015'),
    ('2016', '2016'),
    ('2017', '2017'),
    ('2018', '2018'),
    ('2019', '2019'),
)

AND_OR = (
    ('AND', 'AND'),
    ('OR', 'OR'),
)


###########################################################################
# Class: SemanticSearchForm
###########################################################################

class SemanticSearchForm(forms.Form):
    title = forms.CharField(max_length=150, required=False)
    status = forms.ChoiceField(choices=PROJECT_STATUS, initial='Any', required=False)
    scope = forms.ModelChoiceField(queryset=GeographicalScope.objects.all(), required=False)
    start_year = forms.ChoiceField(choices=YEARS, initial=2004, required=False)
    end_year = forms.ChoiceField(choices=YEARS, initial=2013, required=False)
    researchers = forms.ModelMultipleChoiceField(queryset=Person.objects.all().order_by('full_name'), required=False)
    and_or = forms.ChoiceField(widget=forms.RadioSelect(), choices=AND_OR, required=False)
