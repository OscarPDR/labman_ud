
from entities.persons.models import Job

from datetime import date


####################################################################################################
###     get_person_start_date(assigned_person)
####################################################################################################

def get_person_start_date(assigned_person):
    person_start_date = assigned_person.start_date
    project = assigned_person.project

    try:
        first_job = Job.objects.filter(person=assigned_person.person).order_by('start_date')[0]
        person_first_job = first_job.start_date

    except:
        person_first_job = None

    project_start_date = date(int(project.start_year), int(project.start_month), 1)

    start_dates = []

    if person_start_date:
        start_dates.append(person_start_date)

    if person_first_job:
        start_dates.append(person_first_job)

    if project_start_date:
        start_dates.append(project_start_date)

    return max(start_dates)


####################################################################################################
###     get_person_end_date(assigned_person)
####################################################################################################

def get_person_end_date(assigned_person):
    person_end_date = assigned_person.end_date
    project = assigned_person.project

    try:
        last_job = Job.objects.filter(person=assigned_person.person).order_by('-end_date')[0]
        person_last_job = last_job.end_date

    except:
        person_last_job = None

    project_end_date = date(int(project.end_year), int(project.end_month), 1)
    today = date.today()

    end_dates = []

    if person_end_date:
        end_dates.append(person_end_date)

    if person_last_job:
        end_dates.append(person_last_job)

    if project_end_date:
        end_dates.append(project_end_date)

    if today:
        end_dates.append(today)

    return min(end_dates)
