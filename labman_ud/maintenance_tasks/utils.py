# -*- coding: utf-8 -*-

from django.template.defaultfilters import slugify

from entities.publications.models import PublicationTag
from entities.utils.models import Tag
from entities.projects.models import ProjectTag
from entities.news.models import NewsTag

import json

TAGS_FILEPATH = './files/tag_nicks.json'


def load_tags(path=TAGS_FILEPATH):
    try:
        tags = json.load(open(path, 'r'))

    except:
        print 'Error while loading tag nicks %s' % (TAGS_FILEPATH)

    return tags

# Used to normalize the tags of the papers
# The tag taxonomy is in tag_nicks.json
tag_nicks = load_tags()


def dissambiguate(tag):
    correct_tag = tag
    if tag in tag_nicks.keys():
        correct_tag = tag_nicks[tag]
    return correct_tag.title()


def load_tag_nicks(path='tag_nicks.json'):
    return json.load(open(path, 'r'))


###########################################################################
# def: clean_tags()
###########################################################################
def clean_tags():
    # This tags are only used for metadata, they should not be added to the paper tags
    # We are not using this until we redo the model to include this metadata
    #metadata_tags = ['isi', 'dblp', 'q1', 'q2', 'q3', 'q4', 'corea', 'coreb', 'corec','iwaal', 'phd', 'ucami 2012']
    metadata_tags = ['iwaal', 'phd', 'ucami 2012']
    print
    print 'Cleanning tags...'
    print '#' * 75

    tags = Tag.objects.all()
    tag_names = [t.name for t in tags]

    #************* PUBLICATIONS ***************
    print 'Checking publications...'

    for item in PublicationTag.objects.all():
        curr_tag = item.tag.name

        # Delete the metadata tags
        if (curr_tag.lower() in metadata_tags) or (curr_tag.lower().startswith('jcr')):
            print 'Deleted: %s, %s' % (item.tag.name, item.publication.title)
            item.delete()

        else:
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
    print 'Checking projects...'

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
    print 'Checking news...'

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
