from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from dajaxice.core import dajaxice_functions

from funding_call_manager.models import FundingCall


@dajaxice_register
def get_funding_call(req, pk):
    dajax = Dajax()
    dajax.alert("hey")
    fc = FundingCall.objects.get(pk = pk)
    dajax.assign('#id_funding_program_form-organization', 'value', fc.organization.id)
    dajax.assign('#id_funding_program_form-full_name', 'value', fc.full_name)
    dajax.assign('#id_funding_program_form-short_name', 'value', fc.short_name)
    dajax.assign('#id_funding_program_form-concession_year', 'value', fc.concession_year)
    dajax.assign('#id_funding_program_form-geographical_scope', 'value', str(fc.geographical_scope))
    return dajax.json()
