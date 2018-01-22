# -*- encoding: utf-8 -*-

import threading
import weakref

from inflection import titleize

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.contrib.syndication.views import Feed

from collections import OrderedDict, Counter

from .forms import PersonSearchForm
from .models import Person, Job, AccountProfile

from entities.news.models import News, PersonRelatedToNews
from entities.organizations.models import Organization, Unit
from entities.projects.models import AssignedPerson
from entities.publications.models import Publication, PublicationAuthor
from entities.publications.views import *
from entities.utils.models import Role, Network, PersonRelatedToAward, Award, ProjectRelatedToAward, PublicationRelatedToAward, PersonRelatedToContribution, PersonRelatedToTalkOrCourse
from entities.datasets.models import Dataset, DatasetAuthor


UNIT_ORGANIZATION_IDS = Unit.objects.all().values_list('organization', flat=True)

MEMBER = 'member'
FORMER_MEMBER = 'former_member'


###		__get_person_data(person)
####################################################################################################

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


###		__get_head_data(head)
####################################################################################################

def __get_head_data(head):
    data = __get_person_data(head)

    return {
        'organization': str(data['organization'].short_name),
        'organization_slug': str(data['organization'].slug),
        'full_name': str((head.full_name).encode('utf-8')),
        'gender': str(head.gender),
        'position': str(data['position']),
        'profile_picture_url': str(head.profile_picture.name),
        'slug': str(head.slug),
        'title': str(head.title),
        'profile_konami_code_picture': str(head.profile_konami_code_picture.name),
        'konami_code_position': str(head.konami_code_position),
    }


###		person_index(query_string)
####################################################################################################

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

    # dictionary to be returned in render(request, )
    return_dict = {
        'clean_index': clean_index,
        'form': form,
        'persons': persons,
        'persons_length': persons_length,
        'query_string': query_string,
        'current_page': 'info',
    }

    return render(request, "persons/index.html", return_dict)


###		determine_person_info(person_slug)
####################################################################################################

def determine_person_info(request, person_slug):
    person_status = __determine_person_status(person_slug)

    if person_status == MEMBER:
        return HttpResponseRedirect(reverse('member_info', kwargs={'person_slug': person_slug}))
    if person_status == FORMER_MEMBER:
        return HttpResponseRedirect(reverse('former_member_info', kwargs={'person_slug': person_slug}))
    else:
        return HttpResponseRedirect(reverse('person_info', kwargs={'person_slug': person_slug}))


###		members(organization_slug)
####################################################################################################

def members(request, organization_slug=None):
    konami_positions = []
    konami_profile_pictures = []
    members = []

    organization = None
    units = Unit.objects.all()

    if organization_slug:
        organization = get_object_or_404(Organization, slug=organization_slug)
        filtered_units = Unit.objects.filter(organization=organization)
    else:
        filtered_units = units

    unit_head_person_ids = filtered_units.values_list('head', flat=True).order_by('order')
    unit_head_person_ids = [_id for _id in unit_head_person_ids if _id is not None]

    heads_of_unit = []

    for head_id in unit_head_person_ids:
        head = Person.objects.get(id=head_id)
        heads_of_unit.append(__get_head_data(head))
        konami_positions.append(head.konami_code_position)
        konami_profile_pictures.append(head.profile_konami_code_picture)

    member_list = Person.objects.filter(is_active=True).exclude(id__in=unit_head_person_ids)

    member_list = member_list.order_by('first_surname', 'second_surname', 'first_name')

    for member in member_list:
        member_data = __get_person_data(member)

        if not organization_slug or (organization_slug == member_data['organization'].slug):
            members.append({
                'organization': member_data['organization'].short_name,
                'organization_slug': member_data['organization'].slug,
                'full_name': member.full_name,
                'gender': member.gender,
                'position': member_data['position'],
                'profile_picture_url': member.profile_picture,
                'slug': member.slug,
                'title': member.title,
            })

            konami_positions.append(member.konami_code_position)
            konami_profile_pictures.append(member.profile_konami_code_picture)

    return_dict = {
        'web_title': 'Members',
        'heads_of_unit': heads_of_unit,
        'konami_positions': konami_positions,
        'konami_profile_pictures': konami_profile_pictures,
        'members': members,
        'members_length': len(members) + len(heads_of_unit),
        'units': units,
        'organization': organization,
        'is_active_members': True,
    }

    return render(request, "members/index.html", return_dict)


###		members_redirect()
####################################################################################################

def members_redirect(request):
    return HttpResponseRedirect(reverse('members'))


###		former_members(organization_slug)
####################################################################################################

def former_members(request, organization_slug=None):
    konami_positions = []
    konami_profile_pictures = []
    former_members = []

    organization = None
    units = Unit.objects.all()

    if organization_slug:
        organization = get_object_or_404(Organization, slug=organization_slug)
        filtered_units = Unit.objects.filter(organization=organization)
    else:
        filtered_units = units

    organization_ids = filtered_units.values_list('organization', flat=True)

    organizations = Organization.objects.filter(id__in=organization_ids)

    former_member_ids = Job.objects.filter(
        organization__in=organizations,
        person__is_active=False,
    ).order_by(
        '-end_date',
        'person__full_name',
    ).values_list('person_id', flat=True)

    stacked_person_ids = []

    for _id in former_member_ids:
        if _id not in stacked_person_ids:

            former_member = Person.objects.get(pk=_id)
            former_member_data = __get_person_data(former_member)

            if not organization_slug or (organization_slug == former_member_data['organization'].slug):
                stacked_person_ids.append(_id)

                former_members.append({
                    'organization': former_member_data['organization'].short_name,
                    'organization_slug': former_member_data['organization'].slug,
                    'full_name': former_member.full_name,
                    'gender': former_member.gender,
                    'position': former_member_data['position'],
                    'profile_picture_url': former_member.profile_picture,
                    'slug': former_member.slug,
                    'title': former_member.title,
                })

                konami_positions.append(former_member.konami_code_position)
                konami_profile_pictures.append(former_member.profile_konami_code_picture)

    return_dict = {
        'web_title': 'Former members',
        'konami_positions': konami_positions,
        'konami_profile_pictures': konami_profile_pictures,
        'members': former_members,
        'members_length': len(former_members),
        'units': units,
        'organization': organization,
        'is_active_members': False,
    }

    return render(request, "members/index.html", return_dict)


###		member_info(person_slug)
####################################################################################################

def member_info(request, person_slug):
    units = Unit.objects.all()

    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponsePermanentRedirect(reverse('member_info', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponsePermanentRedirect(reverse('former_member_info', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    return_dict = {
        'web_title': member.full_name,
        'member': member,
        'units': units,
        'current_page': 'info',
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, "members/info.html", return_dict)


###		member_projects(person_slug, role_slug)
####################################################################################################

def member_projects(request, person_slug, role_slug=None):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_projects', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_projects', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    projects = OrderedDict()

    if role_slug:
        roles = [Role.objects.get(slug=role_slug)]
    else:
        roles = Role.objects.all()

    assigned_persons = AssignedPerson.objects.filter(person=member, role__in=roles)

    if assigned_persons:
        has_projects = True

        assigned_persons = assigned_persons.order_by(
            'role__relevance_order',
            '-project__start_year',
            '-project__end_year',
            'project__slug',
        )

        for assigned_person in assigned_persons:
            role_name = assigned_person.role.name

            projects[role_name] = projects.get(role_name, [])
            projects[role_name].append(assigned_person.project)

    else:
        has_projects = False

    return_dict = {
        'has_projects': has_projects,
        'member': member,
        'projects': projects,
        'roles': Role.objects.all(),
        'web_title': u'%s - Projects' % member.full_name,
        'current_page': 'projects',
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, "members/projects.html", return_dict)


###		member_publications(person_slug, publication_type_slug)
####################################################################################################

def member_publications(request, person_slug, publication_type_slug=None):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_publications', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_publications', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    JCR_TITLE = 'JCR indexed journal article'

    publications = OrderedDict()
    publications[JCR_TITLE] = []
    publications['conference-paper'] = []
    publications['book'] = []
    publications['book-section'] = []
    publications['journal-article'] = []
    publications['magazine-article'] = []

    if publication_type_slug:
        publication_type = titleize(publication_type_slug).replace(' ', '')
        publication_ids = member.publications.filter(child_type=publication_type).values_list('id', flat=True)

        if not publication_ids:
            raise Http404
    else:
        publication_ids = member.publications.all().values_list('id', flat=True)

    publication_items = Publication.objects.select_related(
        'conferencepaper',
        'conferencepaper__parent_proceedings',
        'booksection',
        'booksection__parent_book',
        'journalarticle',
        'journalarticle__parent_journal',
        'magazinearticle',
        'magazinearticle__parent_magazine',
    ).prefetch_related('publicationauthor_set__author').filter(id__in=publication_ids).order_by('-published', 'title')

    has_publications = True if publication_ids else False

    for publication_item in publication_items:
        title = publication_item.title
        slug = publication_item.slug
        bibtex = publication_item.bibtex
        year = publication_item.year
        pdf = publication_item.pdf if publication_item.pdf else None

        publication_authors = publication_item.publicationauthor_set.all()
        sorted_publication_authors = sorted(publication_authors, lambda x, y: cmp(x.position, y.position))
        author_list = [pubauthor.author.full_name for pubauthor in sorted_publication_authors]
        authors = ', '.join(author_list)

        parent_title = None
        impact_factor = None

        if publication_item.child_type == 'ConferencePaper':
            conference_paper = publication_item.conferencepaper
            parent_title = conference_paper.parent_proceedings.title if conference_paper.parent_proceedings else ''

        elif publication_item.child_type == 'BookSection':
            book_section = publication_item.booksection
            parent_title = book_section.parent_book.title if book_section.parent_book else ''

        elif publication_item.child_type == 'JournalArticle':
            journal_article = publication_item.journalarticle
            parent_title = journal_article.parent_journal.title if journal_article.parent_journal else ''
            impact_factor = journal_article.parent_journal.impact_factor

        elif publication_item.child_type == 'MagazineArticle':
            magazine_article = publication_item.magazinearticle
            parent_title = magazine_article.parent_magazine.title if magazine_article.parent_magazine else ''

        publication_dict = {
            'title': title,
            'slug': slug,
            'bibtex': bibtex,
            'year': year,
            'pdf': pdf,
            'authors': authors,
            'parent_title': parent_title,
            'impact_factor': impact_factor,
        }

        if publication_item.child_type == 'JournalArticle':
            if journal_article.parent_journal.impact_factor is not None:
                child_type = 'JCR indexed journal article'
            else:
                child_type = 'JournalArticle'
        else:
            child_type = publication_item.child_type

        if not child_type in publications.keys():
            publications[child_type] = []

        publications[child_type].append(publication_dict)

    all_thesis = Thesis.objects.filter(author_id=member.id).all()

    return_dict = {
        'has_publications': has_publications,
        'inside_category': publication_type_slug is not None,
        'member': member,
        'publications': publications,
        'thesis': all_thesis,
        'web_title': u'%s - Publications' % member.full_name,
        'current_page': 'publications',
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, "members/publications.html", return_dict)


###		member_publication_bibtex(person_slug)
####################################################################################################

def member_publication_bibtex(request, person_slug):
    member = get_object_or_404(Person, slug=person_slug)
    global_bibtex = __get_global_bibtex(member)

    return_dict = {
        'web_title': u'%s - Publications bibtex' % member.full_name,
        'member': member,
        'bibtex':  global_bibtex,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, "members/bibtex.html", return_dict)


###		member_publication_bibtex_download(person_slug)
####################################################################################################

def member_publication_bibtex_download(request, person_slug):
    member = get_object_or_404(Person, slug=person_slug)
    global_bibtex = __get_global_bibtex(member)
    response = HttpResponse(global_bibtex, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s.bib"' % member.slug
    return response


###		member_news(person_slug)
####################################################################################################

def member_news(request, person_slug):
    member = get_object_or_404(Person, slug=person_slug)
    person_news_ids = PersonRelatedToNews.objects.filter(person=member).values_list('news_id', flat=True)

    if person_news_ids != []:
        news = News.objects.filter(id__in=person_news_ids).order_by('-created')

    else:
        news = None

    return_dict = {
        'web_title': u'%s - News' % member.full_name,
        'member': member,
        'news': news,
        'current_page': 'news',
    }
    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, 'members/news.html', return_dict)


###		member_awards(person_slug)
####################################################################################################

def member_awards(request, person_slug):
    member = get_object_or_404(Person, slug=person_slug)
    person_awards = PersonRelatedToAward.objects.filter(person=member).select_related('award').order_by('-award__date')
    awards = OrderedDict()

    for award_person in person_awards:
        award = award_person.award
        year_month = u'%s %s' % (award.date.strftime('%B'), award.date.year)
        if not year_month in awards:
            awards[year_month] = []
        awards[year_month].append(award)

    return_dict = {
        'web_title': u'%s - Awards' % member.full_name,
        'member': member,
        'awards': awards,
        'current_page': 'awards',
    }
    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, 'members/awards.html', return_dict)

###		member_datasets(person_slug)
####################################################################################################
def member_datasets(request, person_slug):
    """
    Creates the member datasets view of the personal datasets

    :param request: the information given in the request
    :param person_slug: the person slug
    :return:
    """

    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_datasets', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_datasets', kwargs={'person_slug': person_slug}))

    # Obtaining member information
    member = get_object_or_404(Person, slug=person_slug)
    # Extracting datasets information
    dataset_ids = DatasetAuthor.objects.filter(author=member.id).values_list('dataset_id', flat=True)
    datasets = Dataset.objects.filter(id__in=dataset_ids)

    # Building return dict
    return_dict = {
            'web_title': u'%s - Datasets' % member.full_name,
            'member': member,
            'datasets': datasets,
            'current_page': 'datasets',
            'has_datasets': True if dataset_ids else False,
        }
    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, 'members/datasets.html', return_dict)


###		__get_award_info(award_slug)
####################################################################################################

def __get_award_info(award_slug):
    award = get_object_or_404(Award, slug=award_slug)

    recipient_relations = PersonRelatedToAward.objects.filter(award=award).select_related('person').order_by('id')
    recipients = [recipient_relation.person for recipient_relation in recipient_relations]

    project_relations = ProjectRelatedToAward.objects.filter(award=award).select_related('project')
    projects = [project_relation.project for project_relation in project_relations]

    publication_relations = PublicationRelatedToAward.objects.filter(award=award).select_related('publication')
    publications = [publication_relation.publication for publication_relation in publication_relations]

    return_dict = {
        'award': award,
        'recipients': recipients,
        'related_projects': projects,
        'related_publications': publications,
    }

    return return_dict, award


###     award_info(award_slug)
####################################################################################################

def award_info(request, award_slug):
    return_dict, award = __get_award_info(award_slug)

    return_dict.update({
        'web_title': u'Awards - %s' % award.full_name,
    })

    return render(request, 'awards/info.html', return_dict)


###     award_index()
####################################################################################################

def award_index(request):

    awards = Award.objects.all().order_by('-date')

    return_dict = {
        'web_title': u'Awards',
        'awards': awards,
    }

    return render(request, 'awards/index.html', return_dict)


###     member news feeds(Feed)
####################################################################################################

class LatestUserNewsFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestUserNewsFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    def get_object(self, request, person_slug):
        self.__request.request = weakref.proxy(request)
        return get_object_or_404(Person, slug=person_slug)

    def title(self, obj):
        return "%s news" % obj.full_name

    def link(self, obj):
        url = reverse('member_news', kwargs={'person_slug': obj.slug})
        return self.__request.request.build_absolute_uri(url)

    def description(self, obj):
        return "News about %s" % obj.full_name

    def items(self, obj):
        return PersonRelatedToNews.objects.filter(person=obj).select_related('news').order_by('-news__created')[:30]

    def item_title(self, item):
        return item.news.title

    def item_description(self, item):
        return item.news.content

    def item_link(self, item):
        url = reverse('view_news', args=[item.news.slug])
        return self.__request.request.build_absolute_uri(url)


###     member publications feed(Feed)
####################################################################################################

class LatestUserPublicationFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestUserPublicationFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    def get_object(self, request, person_slug):
        self.__request.request = weakref.proxy(request)
        return get_object_or_404(Person, slug=person_slug)

    def title(self, obj):
        return "%s publications" % obj.full_name

    def link(self, obj):
        url = reverse('member_publications', kwargs={'person_slug': obj.slug})
        return self.__request.request.build_absolute_uri(url)

    def description(self, obj):
        return "Publications where %s is coauthor" % obj.full_name

    def items(self, obj):
        return PublicationAuthor.objects.filter(author=obj).select_related('publication').order_by('-publication__id')[:30]

    def item_title(self, item):
        return item.publication.title

    def item_description(self, item):
        return "New publication: %s " % item.publication.title

    def item_link(self, item):
        url = reverse('publication_info', args=[item.publication.slug])
        return self.__request.request.build_absolute_uri(url)


###		member_profiles(person_slug)
####################################################################################################

def member_profiles(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_profiles', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_profiles', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

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

    return_dict = {
        'member': member,
        'accounts': accounts,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, "members/profiles.html", return_dict)


###		member_graphs(person_slug)
####################################################################################################

def member_graphs(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_graphs', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_graphs', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    # dictionary to be returned in render(request, )
    return_dict = {
        'member': member,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, "members/graphs.html", return_dict)


###		person_info(person_slug)
####################################################################################################

def person_info(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_info', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_info', kwargs={'person_slug': person_slug}))

    person = get_object_or_404(Person, slug=person_slug)

    publication_ids = PublicationAuthor.objects.filter(author=person.id).values('publication_id')
    publications = Publication.objects.filter(id__in=publication_ids).order_by('-year')

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': person.full_name,
        'person': person,
        'publications': publications,
    }

    return render(request, "persons/info.html", return_dict)


###     __determine_person_status(person_slug)
####################################################################################################

def __determine_person_status(person_slug):
    person = get_object_or_404(Person, slug=person_slug)

    if person.is_active:
        return MEMBER

    else:
        organizations = Organization.objects.filter(id__in=UNIT_ORGANIZATION_IDS)
        all_member_ids = Job.objects.filter(organization__in=organizations).values('person_id')
        former_member_list_ids = Person.objects.filter(id__in=all_member_ids, is_active=False).values_list('id', flat=True)

        if person.id in former_member_list_ids:
            return FORMER_MEMBER
        else:
            return None


###     __get_global_bibtex(member)
####################################################################################################

def __get_global_bibtex(member):
    publication_ids = PublicationAuthor.objects.filter(author=member.id).values('publication_id')
    publications_bibtex = Publication.objects.filter(id__in=publication_ids).values_list('bibtex', flat=True).order_by('-year')
    global_bibtex = '\n\n'.join(publications_bibtex)

    return global_bibtex


###     __group_by_key(stmt, key)
####################################################################################################

def __group_by_key(stmt, key='id'):
    """ Given a QuerySet, provide a dictionary grouped by a key. Typically:

    __group_by_key( Foo.objects.all() )

    returns a dictionary where the key is the 'id' field:

    { 1 : FooObject(id=1), 2 : FooObject(id=2) , ... }

    TODO: there is probably something similar in the Django API
    """
    results_by_key = {}
    for result in stmt:
        if isinstance(result, dict):
            results_by_key[result[key]] = result
        else:
            results_by_key[getattr(result, key)] = result
    return results_by_key


###     __get_job_data(member)
####################################################################################################

def __get_job_data(member):
    company = None
    company_slug = None
    first_job = None
    last_job = None
    position = None

    organizations = Organization.objects.filter(id__in=UNIT_ORGANIZATION_IDS)

    try:
        jobs = Job.objects.filter(person_id=member.id, organization_id__in=organizations).order_by('end_date')
        first_job = jobs[0]
        last_job = jobs.reverse()[0]
        organization = Organization.objects.get(id=last_job.organization_id)
        company = organization.short_name
        company_slug = organization.slug
        position = last_job.position
    except:
        pass

    # Extracting datasets information
    dataset_ids = DatasetAuthor.objects.filter(author=member.id).values_list('dataset_id', flat=True)

    project_ids = AssignedPerson.objects.filter(person_id=member.id)
    project_ids = project_ids.order_by('role__relevance_order').values('project_id')

    publication_ids = PublicationAuthor.objects.filter(author=member.id).values_list('publication_id', flat=True)

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

    publication_types = []

    for publication_type in member.publications.all().values_list('child_type', flat=True):
        publication_types.append(titleize(publication_type).lower())

    counter = Counter(publication_types)
    ord_dict = OrderedDict(sorted(counter.items(), key=lambda t: t[1]))

    items = ord_dict.items()

    assigned_persons = AssignedPerson.objects.filter(person=member)
    assigned_persons = assigned_persons.order_by('role__relevance_order',).values_list('role__name', flat=True)

    role_items = OrderedDict()

    for project_role in assigned_persons:
        role_items[project_role] = role_items.get(project_role, 0) + 1

    if Thesis.objects.filter(author_id=member.id).count():
        has_thesis = True
    else:
        has_thesis = False

    if PersonRelatedToAward.objects.filter(person_id=member.id).count():
        has_awards = True
    else:
        has_awards = False

    if PersonRelatedToTalkOrCourse.objects.filter(person_id=member.id).count():
        has_talks = True
    else:
        has_talks = False

    if PersonRelatedToContribution.objects.filter(person_id=member.id).count():
        has_contributions = True
    else:
        has_contributions = False

    if PersonRelatedToNews.objects.filter(person_id=member.id).count():
        has_news = True
    else:
        has_news = False

    if has_awards and has_talks and has_contributions and has_news:
        header_rows = 2
    else:
        header_rows = 1

    if not has_awards and not has_talks and not has_contributions and not has_news and len(project_ids) == 0 \
            and len(publication_ids) == 0 and len(dataset_ids) == 0:
        display_bio = False
    else:
        display_bio = True

    if has_thesis:
        number_of_publications = len(publication_ids) + 1
    else:
        number_of_publications = len(publication_ids)

    return {
        'accounts': accounts,
        'company': company,
        'company_slug': company_slug,
        'display_bio': display_bio,
        'first_job': first_job,
        'has_awards': has_awards,
        'has_contributions': has_contributions,
        'has_news': has_news,
        'has_talks': has_talks,
        'has_thesis': has_thesis,
        'header_rows': header_rows,
        'last_job': last_job,
        'number_of_projects': len(project_ids),
        'number_of_publications': number_of_publications,
        'number_of_datasets': len(dataset_ids),
        'position': position,
        'pubtype_info': dict(items),
        'role_items': role_items,
    }


###		member_phd_dissertation(person_slug)
####################################################################################################

def member_phd_dissertation(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_phd_dissertation', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_phd_dissertation', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    thesis = Thesis.objects.get(author_id=member.id)

    viva_panel = {}

    viva_panel_items = VivaPanel.objects.filter(thesis=thesis)

    for viva_panel_item in viva_panel_items:
        person_name = viva_panel_item.person.full_name
        role = viva_panel_item.role

        viva_panel[person_name] = role

    abstracts = {}

    thesis_abstracts = ThesisAbstract.objects.filter(thesis=thesis)

    for thesis_abstract in thesis_abstracts:
        abstracts[thesis_abstract.language.name] = thesis_abstract.abstract

    has_coadvisors = True if len(thesis.co_advisors.all()) > 0 else False

    return_dict = {
        'abstracts': abstracts,
        'has_coadvisors': has_coadvisors,
        'member': member,
        'thesis': thesis,
        'viva_panel': viva_panel,
        'web_title': u'%s - PhD thesis' % member.full_name,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, "members/phd_dissertation.html", return_dict)


###		member_spanish_cvn(person_slug)
####################################################################################################

def member_spanish_cvn(request, person_slug):

    member = get_object_or_404(Person, slug=person_slug)

    return_dict = {
        'web_title': u'%s - Spanish CVN' % member.full_name,
        'member': member,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render(request, "members/cvn.html", return_dict)
