# -*- coding: utf-8 -*-


from entities.persons.models import Person, Nickname
from entities.publications.models import PublicationAuthor


###########################################################################
# def: check_author_redundancy_through_nicks()
###########################################################################

def check_author_redundancy_through_nicks():
    print '#' * 80
    print 'Checking for author redundancy through nicks...'
    print '#' * 80

    for nick in Nickname.objects.all():
        try:
            bad_person = Person.objects.get(slug=nick.slug)

            if bad_person and bad_person != nick.person:
                print '\tDeleting... %s' % bad_person.full_name

                for pubauth in PublicationAuthor.objects.filter(author=bad_person):
                    print '\tChanging authorship of %s' % pubauth.publication

                    pubauth.author = nick.person
                    pubauth.save()

                bad_person.delete()

        except:
            pass
