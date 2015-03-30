
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from entities.projects.models import Project
from entities.publications.models import Publication
from entities.persons.models import Person
from entities.organizations.models import Organization

register = template.Library()


###     rdf_icon
####################################################################################################

@register.simple_tag
def rdf_icon(entity_object):

    # if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
    if isinstance(entity_object, Project):
        entity_path = u'projects'
    elif isinstance(entity_object, Publication):
        entity_path = u'publications'
    elif isinstance(entity_object, Person):
        entity_path = u'people'
    elif isinstance(entity_object, Organization):
        entity_path = u'organizations'

    rdf_resource_uri = u'%s/%s/%s' % (
        getattr(settings, 'RDF_URI', ''),
        entity_path,
        entity_object.slug,
    )

    rdf_icon_path = u'%simg/rdf.png' % getattr(settings, 'STATIC_URL', '')

    rdf_icon_html_str = """
        <a target='_blank' href='%(rdf_resource_uri)s'>
            <img class='rdf-icon' alt='RDF description' title='RDF description' src='%(rdf_icon_path)s'/>
        </a>
    """ % {
        'rdf_resource_uri': rdf_resource_uri,
        'rdf_icon_path': rdf_icon_path,
    }

    return mark_safe(rdf_icon_html_str)

    # else:
    #     return ''
