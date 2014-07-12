# -*- coding: utf-8 -*-

from entities.publications.models import PublicationTag
from entities.projects.models import ProjectTag
from entities.news.models import NewsTag
from entities.utils.models import Tag


###########################################################################
# def: remove_unrelated_tags()
###########################################################################

def remove_unrelated_tags():
    print '#' * 80
    print 'Checking for unrelated tags to remove...'
    print '#' * 80

    used_tag_ids = set()

    for item in PublicationTag.objects.all():
        used_tag_ids.add(item.tag.id)

    for item in ProjectTag.objects.all():
        used_tag_ids.add(item.tag.id)

    for item in NewsTag.objects.all():
        used_tag_ids.add(item.tag.id)

    unused_tags = Tag.objects.exclude(id__in=used_tag_ids)

    removed_objects = 0

    for tag in unused_tags:
        print '\tTag to be deleted: %s' % tag.name

        tag.delete()
        removed_objects += 1

    print 'Removed %d items' % removed_objects
