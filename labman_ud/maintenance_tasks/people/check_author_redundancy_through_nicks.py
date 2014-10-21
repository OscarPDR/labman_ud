
from entities.events.models import *
from entities.news.models import *
from entities.persons.models import *
from entities.projects.models import *
from entities.publications.models import *
from entities.utils.models import *


###########################################################################
# def: check_author_redundancy_through_nickname_objects()
###########################################################################

def check_author_redundancy_through_nicks(person_object=None):
    print '#' * 80
    print 'Checking for author redundancy through nicknames...'
    print '#' * 80

    if person_object:
        nicknames = Nickname.objects.filter(person=person_object)

    else:
        nicknames = Nickname.objects.all()

    for nickname in nicknames:
        _update_related_fields(nickname)


def _update_related_fields(nickname_object):
    try:
        wrong_person = Person.objects.get(full_name=nickname_object.nickname)

        if (wrong_person) and (wrong_person != nickname_object.person):
            print '\tChecking... %s' % wrong_person.full_name
            print ''

            for item in PersonRelatedToEvent.objects.filter(person=wrong_person):
                print '\t\tUpdating PersonRelatedToEvent() instances'
                item.person = nickname_object.person
                item.save()

            for item in PersonRelatedToNews.objects.filter(person=wrong_person):
                print '\t\tUpdating PersonRelatedToNews() instances'
                item.person = nickname_object.person
                item.save()

            for item in PersonSeeAlso.objects.filter(person=wrong_person):
                print '\t\tUpdating PersonSeeAlso() instances'
                item.person = nickname_object.person
                item.save()

            for item in AccountProfile.objects.filter(person=wrong_person):
                print '\t\tUpdating AccountProfile() instances'
                item.person = nickname_object.person
                item.save()

            for item in Job.objects.filter(person=wrong_person):
                print '\t\tUpdating Job() instances'
                item.person = nickname_object.person
                item.save()

            for item in PhDProgramFollowedByPerson.objects.filter(person=wrong_person):
                print '\t\tUpdating PhDProgramFollowedByPerson() instances'
                item.person = nickname_object.person
                item.save()

            for item in ThesisRegisteredByPerson.objects.filter(person=wrong_person):
                print '\t\tUpdating ThesisRegisteredByPerson() instances'
                item.person = nickname_object.person
                item.save()

            for item in AssignedPerson.objects.filter(person=wrong_person):
                print '\t\tUpdating AssignedPerson() instances'
                item.person = nickname_object.person
                item.save()

            for item in AssignedPersonTag.objects.filter(assigned_person=wrong_person):
                print '\t\tUpdating AssignedPersonTag() instances'
                item.assigned_person = nickname_object.person
                item.save()

            for item in PublicationAuthor.objects.filter(author=wrong_person):
                print '\t\tUpdating PublicationAuthor() instances'
                item.author = nickname_object.person
                item.save()

            for item in PublicationEditor.objects.filter(editor=wrong_person):
                print '\t\tUpdating PublicationEditor() instances'
                item.editor = nickname_object.person
                item.save()

            for item in Thesis.objects.filter(author=wrong_person):
                print '\t\tUpdating Thesis() instances'
                item.author = nickname_object.person
                item.save()

            for item in Thesis.objects.filter(advisor=wrong_person):
                print '\t\tUpdating Thesis() instances'
                item.advisor = nickname_object.person
                item.save()

            for item in CoAdvisor.objects.filter(co_advisor=wrong_person):
                print '\t\tUpdating CoAdvisor() instances'
                item.co_advisor = nickname_object.person
                item.save()

            for item in PersonRelatedToContribution.objects.filter(person=wrong_person):
                print '\t\tUpdating PersonRelatedToContribution() instances'
                item.person = nickname_object.person
                item.save()

            for item in PersonRelatedToTalkOrCourse.objects.filter(person=wrong_person):
                print '\t\tUpdating PersonRelatedToTalkOrCourse() instances'
                item.person = nickname_object.person
                item.save()

            for item in PersonRelatedToAward.objects.filter(person=wrong_person):
                print '\t\tUpdating PersonRelatedToAward() instances'
                item.person = nickname_object.person
                item.save()

            print ''
            print '\tDeleting... %s' % wrong_person.full_name
            wrong_person.delete()

    except:
        pass
