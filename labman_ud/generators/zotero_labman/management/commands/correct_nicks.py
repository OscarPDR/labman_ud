#encoding: utf-8 

from django.core.management.base import NoArgsCommand

from entities.publications.models import PublicationAuthor
from entities.persons.models import Nickname, Person

from generators.zotero_labman.utils import logger

class Command(NoArgsCommand):
    can_import_settings = True

    help = ''

    def handle_noargs(self, **options):
        for nick in Nickname.objects.all():
            try:
		bad_person = Person.objects.get(slug=nick.slug)

                if bad_person and bad_person != nick.person:
		    print 'Deleted... %s' % bad_person.full_name
                    for pubauth in PublicationAuthor.objects.filter(author=bad_person):
			print 'Changing authorship of %s' % pubauth.publication
                        pubauth.author = nick.person
			pubauth.save()
                    bad_person.delete()
	    except:
		pass
