#encoding: utf-8 

from django.core.management.base import NoArgsCommand

from entities.publications.models import PublicationAuthor
from entities.persons.models import Nickname, Person

from generators.zotero_labman.utils import logger

class Command(NoArgsCommand):
    can_import_settings = True

    help = ''

    def handle_noargs(self, **options):
        logger.info('Deleting every publication in DB...')

        for nick in Nickname.objects.all():
            bad_person = Person.objects.get(slug=nick.slug)

            if bad_person:
                for pubauth in PublicationAuthor.objects.filter(author=bad_person):
                    pubauth.author = nick.person
                bad_person.delete()