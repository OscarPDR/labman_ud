from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from funding_programs.models import FundingProgram


@dajaxice_register
def get_funding_call(req, pk):
    dajax = Dajax()
    funding_program = FundingProgram.objects.get(pk = pk)
    dajax.assign('#id_funding_program_form-organization', 'value', funding_program.organization.id)
    dajax.assign('#id_funding_program_form-full_name', 'value', funding_program.full_name)
    dajax.assign('#id_funding_program_form-short_name', 'value', funding_program.short_name)
    dajax.assign('#id_funding_program_form-concession_year', 'value', funding_program.concession_year)
    dajax.assign('#id_funding_program_form-geographical_scope', 'value', str(funding_program.geographical_scope))
    return dajax.json()
