# -*- coding: utf-8 -*-

from entities.events.models import *
from entities.news.models import *
from entities.persons.models import *
from entities.projects.models import *
from entities.publications.models import *
from entities.utils.models import *

from labman_ud.util import get_or_default

import logging
logger = logging.getLogger(__name__)


def _update_related_fields(nickname_object):
    wrong_person = get_or_default(
        Person,
        full_name=nickname_object.nickname,
    )

    if (wrong_person) and (wrong_person != nickname_object.person):

        for item in PersonRelatedToEvent.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating PersonRelatedToEvent() instances')
            item.person = nickname_object.person
            item.save()

        for item in PersonRelatedToNews.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating PersonRelatedToNews() instances')
            item.person = nickname_object.person
            item.save()

        for item in PersonSeeAlso.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating PersonSeeAlso() instances')
            item.person = nickname_object.person
            item.save()

        for item in AccountProfile.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating AccountProfile() instances')
            item.person = nickname_object.person
            item.save()

        for item in Job.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating Job() instances')
            item.person = nickname_object.person
            item.save()

        for item in PhDProgramFollowedByPerson.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating PhDProgramFollowedByPerson() instances')
            item.person = nickname_object.person
            item.save()

        for item in ThesisRegisteredByPerson.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating ThesisRegisteredByPerson() instances')
            item.person = nickname_object.person
            item.save()

        for item in AssignedPerson.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating AssignedPerson() instances')
            item.person = nickname_object.person
            item.save()

        for item in AssignedPersonTag.objects.filter(assigned_person__person=wrong_person):
            logger.info(u'\t\tUpdating AssignedPersonTag() instances')
            item.assigned_person = nickname_object.person
            item.save()

        for item in PublicationAuthor.objects.filter(author=wrong_person):
            logger.info(u'\t\tUpdating PublicationAuthor() instances')
            item.author = nickname_object.person
            item.save()

        for item in PublicationEditor.objects.filter(editor=wrong_person):
            logger.info(u'\t\tUpdating PublicationEditor() instances')
            item.editor = nickname_object.person
            item.save()

        for item in Thesis.objects.filter(author=wrong_person):
            logger.info(u'\t\tUpdating Thesis() instances')
            item.author = nickname_object.person
            item.save()

        for item in Thesis.objects.filter(advisor=wrong_person):
            logger.info(u'\t\tUpdating Thesis() instances')
            item.advisor = nickname_object.person
            item.save()

        for item in CoAdvisor.objects.filter(co_advisor=wrong_person):
            logger.info(u'\t\tUpdating CoAdvisor() instances')
            item.co_advisor = nickname_object.person
            item.save()

        for item in PersonRelatedToContribution.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating PersonRelatedToContribution() instances')
            item.person = nickname_object.person
            item.save()

        for item in PersonRelatedToTalkOrCourse.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating PersonRelatedToTalkOrCourse() instances')
            item.person = nickname_object.person
            item.save()

        for item in PersonRelatedToAward.objects.filter(person=wrong_person):
            logger.info(u'\t\tUpdating PersonRelatedToAward() instances')
            item.person = nickname_object.person
            item.save()

        wrong_person.delete()
        logger.info(u'')
        logger.info(u'\t<%s> instance removed' % wrong_person.full_name)


###     check_people_redundancy(person_object)
####################################################################################################

def check_people_redundancy(person_object=None):

    if person_object:
        logger.info(u'Correcting redundancy only for <%s>' % person_object.full_name)
        nicknames = Nickname.objects.filter(person=person_object)

    else:
        logger.info(u'Correcting redundancy for ALL names in the database')
        nicknames = Nickname.objects.all()

    for nickname in nicknames:
        _update_related_fields(nickname)
