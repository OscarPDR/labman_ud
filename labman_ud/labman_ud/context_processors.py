
from django.conf import settings

from labman_setup.models import *
from entities.publications.models import *
from entities.projects.models import *

from collections import OrderedDict, Counter


####################################################################################################
###     global_vars()
####################################################################################################

def global_vars(request):

    try:
        _settings = LabmanDeployGeneralSettings.objects.get()

    except:
        return {
            'INITIAL_SETUP': True,
        }

    social_profiles = OfficialSocialProfile.objects.all().order_by('name')
    seo_and_analytics = SEOAndAnalytics.objects.first()

    footer_sections = 0
    address_details = False
    contact_details = False
    social_details = False

    if (_settings.address):
        footer_sections += 1
        address_details = True

    if (_settings.email_address or _settings.contact_person or _settings.phone_number):
        footer_sections += 1
        contact_details = True

    if (len(social_profiles) > 0):
        footer_sections += 1
        social_details = True

    if footer_sections in (0, 1):
        footer_divisions_width = 12

    elif footer_sections == 2:
        footer_divisions_width = 6

    else:
        footer_divisions_width = 4

    if (len(social_profiles) <= 3):
        social_profile_width = 3

    elif (len(social_profiles) <= 5):
        social_profile_width = 2

    else:
        social_profile_width = 1

    try:
        twitter_card = TwitterCardsConfiguration.objects.get()

    except:
        twitter_card = None

    twitter_card_image_url = request.build_absolute_uri()

    if twitter_card and twitter_card.card_image:
        twitter_card_image_url += twitter_card.card_image.url

    elif _settings.research_group_official_logo:
        twitter_card_image_url += _settings.research_group_official_logo.url

    else:
        twitter_card_image_url = None

    if twitter_card_image_url:
        twitter_card_image_url = twitter_card_image_url.replace("//", "/")

    publication_types = Publication.objects.all().exclude(authors=None).values_list('child_type', flat=True)
    publication_counter = Counter(publication_types)
    publication_dict = OrderedDict(sorted(publication_counter.items(), key=lambda t: t[1]))
    publication_items = publication_dict.items()

    try:
        theses = Thesis.objects.all()

    except:
        theses = None

    project_types = Project.objects.all().values_list('project_type', flat=True)
    project_counter = Counter(project_types)
    project_dict = OrderedDict(sorted(project_counter.items(), key=lambda t: t[1]))
    project_items = project_dict.items()

    about_section_titles = AboutSection.objects.all().order_by('order').values_list('title', flat=True)

    return_dict = {
        'ADDRESS_DETAILS': address_details,
        'BASE_URL': getattr(settings, 'BASE_URL', None),
        'CONTACT_DETAILS': contact_details,
        'ENABLE_RDF_PUBLISHING': getattr(settings, 'ENABLE_RDF_PUBLISHING', False),
        'FOOTER_DIVISIONS_WIDTH': footer_divisions_width,
        'RDF_URI': getattr(settings, 'GRAPH_BASE_URL', '') + '/',
        'RESEARCH_GROUP_SETTINGS': _settings,
        'SEO_AND_ANALYTICS': seo_and_analytics,
        'SOCIAL_DETAILS': social_details,
        'SOCIAL_PROFILE_WIDTH': social_profile_width,
        'SOCIAL_PROFILES': social_profiles,
        'TWITTER_CARD': twitter_card,
        'TWITTER_CARD_IMAGE': twitter_card_image_url,
        'NUMBER_OF_PUBLICATIONS': len(publication_types),
        'PUBLICATION_TYPES': dict(publication_items),
        'NUMBER_OF_PROJECTS': len(project_types),
        'PROJECT_TYPES': dict(project_items),
        'THESES': theses,
        'ABOUT_SECTION_TITLES': about_section_titles,
    }

    return return_dict
