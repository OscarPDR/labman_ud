# -*- coding: utf-8 -*-

from django.template.defaultfilters import slugify

from entities.news.models import NewsTag
from entities.projects.models import ProjectTag
from entities.publications.models import PublicationTag
from entities.utils.models import Tag

from django.conf import settings

import json


TAGS_FILEPATH = '%s/static/%s' % (getattr(settings, 'PROJECT_DIR', None), 'json/tag_nicks.json')


###########################################################################
# def: load_tags()
###########################################################################

def load_tags():
    try:
        tags = json.load(open(TAGS_FILEPATH, 'r'))

    except:
        print 'Error while loading tag nicks %s' % (TAGS_FILEPATH)

    return tags


###########################################################################
# def: dissambiguate()
###########################################################################

def dissambiguate(tag):
    # Used to normalize the tags of the papers
    # The tag taxonomy is in tag_nicks.json
    tag_nicks = load_tags()

    correct_tag = tag
    if tag in tag_nicks.keys():
        correct_tag = tag_nicks[tag]
    return correct_tag.title()


###########################################################################
# def: clean_tags()
###########################################################################

def clean_tags():
    print
    print 'Cleanning tags...'
    print '#' * 80

    tag_names = Tag.objects.all().values_list('name', flat=True)

    #************* PUBLICATIONS ***************
    print
    print 'Checking publications...'
    print '#' * 80

    for item in PublicationTag.objects.all():
        curr_tag = item.tag.name

        diss_tag = dissambiguate(curr_tag)
        # Tag needs to be dissambiguated

        if curr_tag != diss_tag:
            tag = item.tag
            publication = item.publication
            # Dissambiguated tag does not exists

            if not diss_tag in tag_names:
                try:
                    t = Tag(name=diss_tag, slug=slugify(diss_tag))
                    t.save()
                    tag = t

                    print 'Created new tag: %s' % (diss_tag)

                except:
                    tag = Tag.objects.filter(slug__exact=slugify(diss_tag))[0]
                    tag.name = diss_tag
                    tag.save()

            else:
                tag = Tag.objects.filter(slug__exact=slugify(diss_tag))[0]

            # Delete the old tag-pub association
            print 'Deleted: %s, %s' % (item.tag.name, item.publication.title)

            item.delete()

            # Create new tag-pub association
            pt = PublicationTag(tag=tag, publication=publication)
            pt.save()

    #************* PROJECTS ***************
    print
    print 'Checking projects...'
    print '#' * 80

    for item in ProjectTag.objects.all():
        curr_tag = item.tag.name
        diss_tag = dissambiguate(curr_tag)
        # Tag needs to be dissambiguated

        if curr_tag != diss_tag:
            tag = item.tag
            project = item.project
            # Dissambiguated tag does not exists

            if not diss_tag in tag_names:
                try:
                    t = Tag(name=diss_tag, slug=slugify(diss_tag))
                    t.save()
                    tag = t

                    print 'Created new tag: %s' % (diss_tag)

                except:
                    tag = Tag.objects.filter(slug__exact=slugify(diss_tag))[0]
                    tag.name = diss_tag
                    tag.save()

            else:
                tag = Tag.objects.filter(slug__exact=slugify(diss_tag))[0]

            # Delete the old news-pub association
            print 'Deleted: %s, %s' % (item.tag.name, item.project.full_name)

            item.delete()

            # Create new news-pub association
            if type(tag) != Tag:
                print tag, type(tag)

            pt = ProjectTag(tag=tag, project=project)
            pt.save()

    #************* NEWS ***************
    print
    print 'Checking news...'
    print '#' * 80

    for item in NewsTag.objects.all():
        curr_tag = item.tag.name
        diss_tag = dissambiguate(curr_tag)
        # Tag needs to be dissambiguated

        if curr_tag != diss_tag:
            tag = item.tag
            news = item.news
            # Dissambiguated tag does not exists

            if not diss_tag in tag_names:
                try:
                    t = Tag(name=diss_tag, slug=slugify(diss_tag))
                    t.save()
                    tag = t

                    print 'Created new tag: %s' % (diss_tag)

                except:
                    tag = Tag.objects.filter(slug__exact=slugify(diss_tag))[0]
                    tag.name = diss_tag
                    tag.save()

            else:
                tag = Tag.objects.filter(slug__exact=slugify(diss_tag))[0]

            # Delete the old news-pub association
            print 'Deleted: %s, %s' % (item.tag.name, item.news.title)

            item.delete()

            # Create new news-pub association
            pt = NewsTag(tag=tag, news=news)
            pt.save()

    print 'Done'
