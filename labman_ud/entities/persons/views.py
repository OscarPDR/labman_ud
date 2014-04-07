# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify

from collections import OrderedDict, defaultdict

from .forms import PersonSearchForm
from .models import Person, Job, AccountProfile

from entities.organizations.models import Organization
from entities.projects.models import Project, AssignedPerson
from entities.publications.models import Publication, PublicationType, PublicationAuthor, PublicationTag
from entities.utils.models import Role, Tag, Network
from entities.publications.views import INDICATORS_TAG_SLUGS

# Create your views here.

REMOVABLE_TAGS = ['ISI', 'corea', 'coreb', 'corec', 'Q1', 'Q2']

OWN_ORGANIZATION_SLUGS = ['deustotech-internet', 'deustotech-telecom', 'morelab']

# Status
MEMBER = 'member'
FORMER_MEMBER = 'former_member'


###########################################################################
# View: __get_person_data
###########################################################################

def __get_person_data(person):
    try:
        job = Job.objects.filter(person_id=person.id).order_by('-end_date')[0]
        organization = Organization.objects.get(id=job.organization_id)
        position = job.position

    except:
        organization = None
        position = None

    return {
        'person': person,
        'organization': organization,
        'position': position,
    }


###########################################################################
# View: __get_head_data
###########################################################################

def __get_head_data(head):
    data = __get_person_data(head)

    return {
        'company': str(data['organization'].short_name),
        'full_name': str((head.full_name).encode('utf-8')),
        'gender': str(head.gender),
        'position': str(data['position']),
        'profile_picture_url': str(head.profile_picture.name),
        'slug': str(head.slug),
        'title': str(head.title),
        'profile_konami_code_picture': str(head.profile_konami_code_picture.name),
        'konami_code_position': str(head.konami_code_position),
    }


###########################################################################
# View: person_index
###########################################################################

def person_index(request, query_string=None):
    clean_index = True

    if query_string:
        query = slugify(query_string)
        persons = Person.objects.filter(slug__contains=query)
        clean_index = False
    else:
        persons = Person.objects.all()

    persons = persons.order_by('full_name')

    if request.method == 'POST':
        form = PersonSearchForm(request.POST)

        if form.is_valid():
            query_string = form.cleaned_data['text']
            clean_index = False

            return HttpResponseRedirect(reverse('view_person_query', kwargs={'query_string': query_string}))

    else:
        form = PersonSearchForm()

    persons_length = len(persons)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'clean_index': clean_index,
        'form': form,
        'persons': persons,
        'persons_length': persons_length,
        'query_string': query_string,
    }

    return render_to_response("persons/index.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: determine_person_info
###########################################################################

def determine_person_info(request, person_slug):
    person_status = __determine_person_status(person_slug)

    if person_status == MEMBER:
        return HttpResponseRedirect(reverse('member_info', kwargs={'person_slug': person_slug}))
    if person_status == FORMER_MEMBER:
        return HttpResponseRedirect(reverse('former_member_info', kwargs={'person_slug': person_slug}))
    else:
        return HttpResponseRedirect(reverse('person_info', kwargs={'person_slug': person_slug}))


###########################################################################
# View: members
###########################################################################

def members(request, organization_slug=None):
    member_konami_positions = []
    member_konami_profile_pictures = []
    members = []

    # MORElab only
    pr_internet = Person.objects.get(full_name='Diego López-de-Ipiña')
    head_of_internet = __get_head_data(pr_internet)

    pr_telecom = Person.objects.get(first_name='Jon', first_surname='Legarda')
    head_of_telecom = __get_head_data(pr_telecom)

    member_list = Person.objects.filter(is_active=True).exclude(id__in=[pr_internet.id, pr_telecom.id])
    member_list = member_list.order_by('first_surname', 'second_surname', 'first_name')
    # End of MORElab only

    for member in member_list:
        member_data = __get_person_data(member)

        if not organization_slug or (organization_slug == member_data['organization'].slug):
            members.append({
                'company': member_data['organization'].short_name,
                'full_name': member.full_name,
                'gender': member.gender,
                'position': member_data['position'],
                'profile_picture_url': member.profile_picture,
                'slug': member.slug,
                'title': member.title,
            })

            member_konami_positions.append(member.konami_code_position)
            member_konami_profile_pictures.append(member.profile_konami_code_picture)

    if organization_slug:
        organization = Organization.objects.get(slug=organization_slug)
    else:
        organization = None

    # dictionary to be returned in render_to_response()
    return_dict = {
        'head_of_internet': head_of_internet,
        'head_of_telecom': head_of_telecom,
        'member_konami_positions': member_konami_positions,
        'member_konami_profile_pictures': member_konami_profile_pictures,
        'members': members,
        'organization': organization,
        'organization_slug': organization_slug,
    }

    return render_to_response("members/members_index.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: former_members
###########################################################################

def former_members(request, organization_slug=None):

    former_member_konami_positions = []
    former_member_konami_profile_pictures = []
    former_members = []

    organizations = Organization.objects.filter(slug__in=OWN_ORGANIZATION_SLUGS)

    former_member_ids = Job.objects.filter(organization__in=organizations).values('person_id')

    former_member_list = Person.objects.filter(id__in=former_member_ids, is_active=False)
    former_member_list = former_member_list.order_by('first_surname', 'second_surname', 'first_name')

    former = {}
    ordered_dict = OrderedDict()

    for former_member in former_member_list:
        job = Job.objects.filter(person_id=former_member.id).order_by('-end_date')[0]

        if not job.end_date in former.keys():
            former[job.end_date] = []

        former[job.end_date].append(former_member)

    ordered_dict = OrderedDict(sorted(former.items(), key=lambda t: t[0], reverse=True))

    former_member_list = []

    for value in ordered_dict.values():
        for item in value:
            former_member_list.append(item)

    for former_member in former_member_list:
        job = Job.objects.filter(person_id=former_member.id).order_by('-end_date')[0]
        organization = Organization.objects.get(id=job.organization_id)

        if not organization_slug or (organization_slug == organization.slug):
            former_members.append({
                'company': organization.short_name,
                'full_name': former_member.full_name,
                'gender': former_member.gender,
                'position': job.position,
                'profile_picture_url': former_member.profile_picture,
                'slug': former_member.slug,
                'title': former_member.title,
            })

            former_member_konami_positions.append(former_member.konami_code_position)
            former_member_konami_profile_pictures.append(former_member.profile_konami_code_picture)

    if organization_slug:
        organization = Organization.objects.get(slug=organization_slug)
    else:
        organization = None

    # dictionary to be returned in render_to_response()
    return_dict = {
        'former_member_konami_positions': former_member_konami_positions,
        'former_member_konami_profile_pictures': former_member_konami_profile_pictures,
        'former_members': former_members,
        'organization': organization,
        'organizations': organizations,
    }

    return render_to_response("members/former_members_index.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_info
###########################################################################

def member_info(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_info', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_info', kwargs={'person_slug': person_slug}))

    member = Person.objects.get(slug=person_slug)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'member': member,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/info.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_projects
###########################################################################

def member_projects(request, person_slug, role_slug=None):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_projects', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_projects', kwargs={'person_slug': person_slug}))

    member = Person.objects.get(slug=person_slug)

    projects = {}

    has_projects = False

    if role_slug:
        roles = [Role.objects.get(slug=role_slug)]
    else:
        roles = Role.objects.all()

    for role in roles:
        projects[role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=member.id, role=role.id).values('project_id')
        if project_ids:
            has_projects = True
        project_objects = Project.objects.filter(id__in=project_ids).order_by('-start_year', '-end_year')

        for project in project_objects:
            projects[role.name].append(project)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'member': member,
        'has_projects': has_projects,
        'projects': projects,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/projects.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_publications
###########################################################################

def member_publications(request, person_slug, publication_type_slug=None):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_publications', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_publications', kwargs={'person_slug': person_slug}))

    member = Person.objects.get(slug=person_slug)

    publications = OrderedDict()

    publication_ids = PublicationAuthor.objects.filter(author=member.id).values('publication_id')
    # Get those tags which are indicators (ISI, JCR...)
    tags = Tag.objects.filter(slug__in=INDICATORS_TAG_SLUGS).values('id','slug')
    tags_by_slug = {}
    for tag in tags:
        tags_by_slug[tag['slug']] = tag['id']

    publication_tag_ids = PublicationTag.objects.filter(publication_id__in=publication_ids, tag__slug__in=INDICATORS_TAG_SLUGS).values('tag_id','publication_id')
    indicators_per_publication = defaultdict(list)
    for publication_tag_id in publication_tag_ids:
        indicators_per_publication[publication_tag_id['publication_id']].append(publication_tag_id['tag_id'])
        

    has_publications = True if publication_ids else False

    jcr_name = 'JCR article'
    isi_name = 'ISI article'
    SEPARATE_ISI = False

    if publication_type_slug:
        publication_types = [PublicationType.objects.get(slug=publication_type_slug)]
        publication_query = Publication.objects.filter(id__in=publication_ids, publication_type__in=publication_types).order_by('-year') 
    else:
        publication_types = PublicationType.objects.all()

        SPECIAL_ORDER = ['phd-thesis', jcr_name, isi_name, 'journal-article', 'conference'] # The rest afterwards
        
        for current_key in SPECIAL_ORDER:
    
            found = False

            for publication_type in publication_types:
                if publication_type.slug == current_key:
                    publications[publication_type.name.encode('utf-8')] = []
                    found = True
                    break

            # Some keys do not really exist (such as JCR). Put it in that order anyway

            if not found:
                publications[current_key] = []

        publication_query = Publication.objects.filter(id__in=publication_ids).order_by('-year') 

    tag_names = {
        'q1' : jcr_name,
        'q2' : jcr_name,
        'q3' : jcr_name,
        'q4' : jcr_name,

    }

    if SEPARATE_ISI:
        tag_names['isi'] = isi_name

    for publication in publication_query:
        for tag_slug in tag_names:
            if tags_by_slug.get(tag_slug, -1) in indicators_per_publication[publication.id]:
                pub_type = tag_names[tag_slug]
                break
        else:
            pub_type = publication.publication_type.name.encode('utf-8')

        if pub_type not in publications:
            publications[pub_type] = []
        publications[pub_type].append(publication)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'member': member,
        'publications': publications,
        'has_publications': has_publications,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/publications.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_profiles
###########################################################################

def member_profiles(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_profiles', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_profiles', kwargs={'person_slug': person_slug}))

    member = Person.objects.get(slug=person_slug)

    accounts = []
    account_profiles = AccountProfile.objects.filter(person_id=member.id).order_by('network__name')

    for account_profile in account_profiles:
        network = Network.objects.get(id=account_profile.network_id)
        account_item = {
            'base_url': network.base_url,
            'icon_url': network.icon,
            'network_name': network.name,
            'profile_id': account_profile.profile_id,
        }
        accounts.append(account_item)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'member': member,
        'accounts': accounts,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/profiles.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_graphs
###########################################################################

def member_graphs(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_graphs', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_graphs', kwargs={'person_slug': person_slug}))

    member = Person.objects.get(slug=person_slug)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'member': member,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/graphs.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: person_info
###########################################################################

def person_info(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_info', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_info', kwargs={'person_slug': person_slug}))

    person = Person.objects.get(slug=person_slug)

    projects = {}

    roles = Role.objects.all()

    for role in roles:
        projects[role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=person.id, role=role.id).values('project_id')
        project_objects = Project.objects.filter(id__in=project_ids).order_by('slug')

        for project in project_objects:
            projects[role.name].append(project)

    publication_ids = PublicationAuthor.objects.filter(author=person.id).values('publication_id')
    _publications = Publication.objects.filter(id__in=publication_ids).order_by('-year')

    publications = {}

    for publication_type in PublicationType.objects.all():
        pub_type = publication_type.name.encode('utf-8')
        publications[pub_type] = []

    for publication in _publications:
        pub_type = publication.publication_type.name.encode('utf-8')
        publications[pub_type].append(publication)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'person': person,
        'projects': projects,
        'publications': publications,
    }

    return render_to_response("persons/info.html", return_dict, context_instance=RequestContext(request))


####################################################################################################
# __clean_publication_tags
####################################################################################################

def __clean_publication_tags(member_id, min_year, max_year):
    publication_ids = PublicationAuthor.objects.filter(author_id=member_id).values('publication_id')

    pub_tag_ids = PublicationTag.objects.filter(publication_id__in=publication_ids).values('tag_id')
    all_pub_tags = PublicationTag.objects.filter(publication_id__in=publication_ids).values('tag_id__name', 'publication_id__year')
    pub_tags = Tag.objects.filter(id__in=pub_tag_ids).values_list('name', flat=True).distinct()

    tags = [x for x in pub_tags if x not in REMOVABLE_TAGS]

    publication_tags_per_year = {}

    for t in tags:
        tag = t.encode('utf-8')
        publication_tags_per_year[tag] = {}

        for year in range(min_year, max_year + 1):
            publication_tags_per_year[tag][year] = 0

    for pub_tag in all_pub_tags:
        try:
            tag_name = pub_tag.get('tag_id__name').encode('utf-8')
            year = pub_tag.get('publication_id__year')

            publication_tags_per_year[tag_name][year] = publication_tags_per_year[tag_name][year] + 1

        except:
            pass

    return publication_tags_per_year


####################################################################################################
# __determine_person_status
####################################################################################################

def __determine_person_status(person_slug):
    person = Person.objects.get(slug=person_slug)
    if person.is_active:
        return MEMBER
    else:
        organizations = Organization.objects.filter(slug__in=OWN_ORGANIZATION_SLUGS)
        all_member_ids = Job.objects.filter(organization__in=organizations).values('person_id')
        former_member_list_ids = Person.objects.filter(id__in=all_member_ids, is_active=False).values_list('id', flat=True)

        if person.id in former_member_list_ids:
            return FORMER_MEMBER
        else:
            return None


####################################################################################################
# __get_job_data
####################################################################################################

def __get_job_data(member):
    company = None
    first_job = None
    last_job = None
    position = None

    organizations = Organization.objects.filter(slug__in=OWN_ORGANIZATION_SLUGS)

    try:
        jobs = Job.objects.filter(person_id=member.id, organization_id__in=organizations).order_by('end_date')
        first_job = jobs[0]
        last_job = jobs.reverse()[0]
        organization = Organization.objects.get(id=last_job.organization_id)
        company = organization.short_name
        position = last_job.position
    except:
        pass

    pr_role = Role.objects.get(slug='principal-researcher')
    project_ids = AssignedPerson.objects.filter(person_id=member.id).exclude(role_id=pr_role.id).values('project_id')
    publication_ids = PublicationAuthor.objects.filter(author=member.id).values('publication_id')

    accounts = []
    account_profiles = AccountProfile.objects.filter(person_id=member.id).order_by('network__name')

    for account_profile in account_profiles:
        network = Network.objects.get(id=account_profile.network_id)
        account_item = {
            'base_url': network.base_url,
            'icon_url': network.icon,
            'network_name': network.name,
            'profile_id': account_profile.profile_id,
        }
        accounts.append(account_item)


    return {
        'first_job': first_job,
        'last_job': last_job,
        'company': company,
        'position': position,
        'number_of_projects': len(project_ids),
        'number_of_publications': len(publication_ids),
        'accounts' : accounts,
    }
