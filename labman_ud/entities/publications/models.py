# -*- encoding: utf-8 -*-

import os

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from entities.core.models import BaseModel

from .linked_data import *

from redactor.fields import RedactorField

# Create your models here.

MIN_YEAR_LIMIT = 1950
MAX_YEAR_LIMIT = 2080

CORE_CHOICES = (
    ('A', 'Core A'),
    ('B', 'Core B'),
    ('C', 'Core C'),
    (None, 'None'),
)

QUARTILE_CHOICES = (
    ('Q1', 'Q1'),
    ('Q2', 'Q2'),
    ('Q3', 'Q3'),
    ('Q4', 'Q4'),
    (None, 'None'),
)

VIVA_OUTCOMES = (
    ('Apt', 'Apt'),
    ('Cum Laude', 'Cum Laude'),
    ('Cum Laude by unanimity', 'Cum Laude by unanimity'),
)

VIVA_PANEL_ROLES = (
    ('Chair', 'Chair'),
    ('Secretary', 'Secretary'),
    ('Co-chair', 'Co-chair'),
    ('First co-chair', 'First co-chair'),
    ('Second co-chair', 'Second co-chair'),
    ('Third co-chair', 'Third co-chair'),
    ('Vocal', 'Vocal'),
)


def publication_path(self, filename):
    publication_type_slug = slugify(self.child_type)

    sub_folder = publication_type_slug

    try:
        sub_folder = '%s/%s' % (sub_folder, self.presented_at.slug)
    except:
        pass

    return "%s/%s/%s/%s%s" % ("publications", self.published.year, sub_folder, self.slug, os.path.splitext(filename)[-1])


def thesis_path(self, filename):
    return "%s/%s/%s%s" % ("publications", "theses", self.author.slug, os.path.splitext(filename)[-1])


def ranking_icon_picture_path(self, filename):
    return "%s/%s%s" % ("rankings", self.slug, os.path.splitext(filename)[-1])


###########################################################################
# Model: Publication
###########################################################################

class Publication(BaseModel):
    title = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
    )

    abstract = models.TextField(
        max_length=2500,
        blank=True,
        null=True,
    )

    doi = models.CharField(
        max_length=100,
        verbose_name=u'DOI',
        blank=True,
        null=True,
    )

    published = models.DateField(
        blank=True,
        null=True,
    )

    year = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
    )

    pdf = models.FileField(
        max_length=1000,
        upload_to=publication_path,
        blank=True,
        null=True,
    )

    language = models.ForeignKey(
        'utils.Language',
        blank=True,
        null=True,
    )

    bibtex = models.TextField(
        max_length=2500,
        blank=True,
        null=True,
    )

    child_type = models.CharField(
        max_length=50,
        blank=True,
    )

    authors = models.ManyToManyField('persons.Person', through='PublicationAuthor', related_name='authors')
    editors = models.ManyToManyField('persons.Person', through='PublicationEditor', related_name='editors')
    tags = models.ManyToManyField('utils.Tag', through='PublicationTag')
    rankings = models.ManyToManyField('Ranking', through='PublicationRank')

    class Meta:
        # abstract = True
        ordering = ['-slug']
        verbose_name = u'Publication'
        verbose_name_plural = u'Publications'

    def display_all_fields(self):
        all_fields = [
            self.title,
            self.slug,
            # self.abstract,
        ]

        for author in self.authors.all():
            all_fields.append(author.full_name)

        for tag in self.tags.all():
            all_fields.append(tag.name)

        return u' '.join([field for field in all_fields if field])

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        old_slug = self.slug

        self.slug = slugify(str(self.title.encode('utf-8')))

        if self.child_type == '':
            self.child_type = self.__class__.__name__

        super(Publication, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_publication_as_rdf(self)
            update_publication_object_triples(old_slug, self.slug)


###########################################################################
# Model: PublicationSeeAlso
###########################################################################

class PublicationSeeAlso(BaseModel):
    publication = models.ForeignKey('Publication')

    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.publication.title, self.see_also)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_publication_see_also_rdf(self)

        super(PublicationSeeAlso, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_publication_see_also_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_publication_see_also_rdf(self)

        super(PublicationSeeAlso, self).delete(*args, **kwargs)


###########################################################################
# Model: CollectionPublication
###########################################################################

class CollectionPublication(Publication):
    publisher = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )

    place = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )

    volume = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


###########################################################################
# Model: PartOfCollectionPublication
###########################################################################

class PartOfCollectionPublication(Publication):
    pages = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )

    short_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


###########################################################################
# Model: ISIDBLPTags
###########################################################################

class ISIDBLPTags(PartOfCollectionPublication):
    isi = models.BooleanField(
        verbose_name=u'ISI',
        default=False,
    )

    dblp = models.BooleanField(
        verbose_name=u'DBLP',
        default=False,
    )

    class Meta:
        abstract = True


###########################################################################
# Model: Book
###########################################################################

class Book(CollectionPublication):
    isbn = models.CharField(
        max_length=100,
        verbose_name=u'ISBN',
        blank=True,
        null=True,
    )

    edition = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    series = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )

    series_number = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    number_of_pages = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    number_of_volumes = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'Book'
        verbose_name_plural = u'Books'

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_book_rdf(self)

        super(Book, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_book_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_book_rdf(self)

        super(Book, self).delete(*args, **kwargs)


###########################################################################
# Model: BookSection
###########################################################################

class BookSection(ISIDBLPTags):
    parent_book = models.ForeignKey('Book')

    presented_at = models.ForeignKey('events.Event', null=True, blank=True)

    core = models.CharField(
        max_length=25,
        choices=CORE_CHOICES,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'Book section'
        verbose_name_plural = u'Book sections'

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_book_section_rdf(self)

        super(BookSection, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_book_section_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_book_section_rdf(self)

        super(BookSection, self).delete(*args, **kwargs)


###########################################################################
# Model: Proceedings
###########################################################################

class Proceedings(CollectionPublication):
    isbn = models.CharField(
        max_length=100,
        verbose_name=u'ISBN',
        blank=True,
        null=True,
    )

    series = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'Proceedings item'
        verbose_name_plural = u'Proceedings'

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_proceedings_rdf(self)

        super(Proceedings, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_proceedings_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_proceedings_rdf(self)

        super(Proceedings, self).delete(*args, **kwargs)


###########################################################################
# Model: ConferencePaper
###########################################################################

class ConferencePaper(ISIDBLPTags):
    parent_proceedings = models.ForeignKey('Proceedings')

    presented_at = models.ForeignKey(
        'events.Event',
        blank=True,
        null=True,
    )

    core = models.CharField(
        max_length=25,
        choices=CORE_CHOICES,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'Conference paper'
        verbose_name_plural = u'Conference papers'

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_conference_paper_rdf(self)

        super(ConferencePaper, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_conference_paper_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_conference_paper_rdf(self)

        super(ConferencePaper, self).delete(*args, **kwargs)


###########################################################################
# Model: Journal
###########################################################################

class Journal(CollectionPublication):
    issn = models.CharField(
        max_length=100,
        verbose_name=u'ISSN',
        blank=True,
        null=True,
    )

    issue = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    journal_abbreviation = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    quartile = models.CharField(
        max_length=25,
        choices=QUARTILE_CHOICES,
        default=None,
        blank=True,
        null=True,
    )

    impact_factor = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'Journal'
        verbose_name_plural = u'Journals'

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_journal_rdf(self)

        super(Journal, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_journal_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_journal_rdf(self)

        super(Journal, self).delete(*args, **kwargs)


###########################################################################
# Model: JournalArticle
###########################################################################

class JournalArticle(ISIDBLPTags):
    parent_journal = models.ForeignKey('Journal')

    individually_published = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'Journal article'
        verbose_name_plural = u'Journal articles'

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_journal_article_rdf(self)

        super(JournalArticle, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_journal_article_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_journal_article_rdf(self)

        super(JournalArticle, self).delete(*args, **kwargs)


###########################################################################
# Model: Magazine
###########################################################################

class Magazine(CollectionPublication):
    issn = models.CharField(
        max_length=100,
        verbose_name=u'ISSN',
        blank=True,
        null=True,
    )

    issue = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'Magazine'
        verbose_name_plural = u'Magazines'

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_magazine_rdf(self)

        super(Magazine, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_magazine_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_magazine_rdf(self)

        super(Magazine, self).delete(*args, **kwargs)


###########################################################################
# Model: MagazineArticle
###########################################################################

class MagazineArticle(PartOfCollectionPublication):
    parent_magazine = models.ForeignKey('Magazine')

    class Meta:
        verbose_name = u'Magazine article'
        verbose_name_plural = u'Magazine articles'

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_magazine_article_rdf(self)

        super(MagazineArticle, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_magazine_article_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_magazine_article_rdf(self)

        super(MagazineArticle, self).delete(*args, **kwargs)


###########################################################################
# Model: PublicationTag
###########################################################################

class PublicationTag(BaseModel):
    tag = models.ForeignKey('utils.Tag')
    publication = models.ForeignKey('publications.Publication')

    class Meta:
        verbose_name = u'Publication tag'
        verbose_name_plural = u'Publication tags'

    class Meta:
        ordering = ['tag__slug']

    def __unicode__(self):
        return u'%s tagged as: %s' % (self.publication.title, self.tag.name)


###########################################################################
# Model: PublicationAuthor
###########################################################################

class PublicationAuthor(BaseModel):
    author = models.ForeignKey('persons.Person')

    publication = models.ForeignKey('publications.Publication')

    position = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'Publication author'
        verbose_name_plural = u'Publication authors'

    def __unicode__(self):
        return u'%s has written: %s as author #%d' % (self.author.full_name, self.publication.title, self.position)


###########################################################################
# Model: PublicationEditor
###########################################################################

class PublicationEditor(BaseModel):
    editor = models.ForeignKey('persons.Person')

    publication = models.ForeignKey('publications.Publication')

    class Meta:
        verbose_name = u'Publication editor'
        verbose_name_plural = u'Publication editors'

    def __unicode__(self):
        return u'%s has edited: %s' % (self.editor.full_name, self.publication.title)


###########################################################################
# Model: Thesis
###########################################################################

class Thesis(BaseModel):
    title = models.CharField(
        max_length=1000,
    )

    author = models.ForeignKey('persons.Person', related_name='has_thesis')

    slug = models.SlugField(
        max_length=255,
        blank=True,
        unique=True,
    )

    advisor = models.ForeignKey(
        'persons.Person',
        related_name='advised_thesis',
    )

    co_advisors = models.ManyToManyField(
        'persons.Person',
        blank=True,
        null=True,
        through='CoAdvisor',
        related_name='coadvised_thesis',
    )

    registration_date = models.DateField(
        blank=True,
        null=True,
    )

    year = models.PositiveIntegerField()

    main_language = models.ForeignKey('utils.Language')

    # topics

    pdf = models.FileField(
        upload_to=thesis_path,
        blank=True,
        null=True,
    )

    number_of_pages = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    viva_date = models.DateTimeField()

    viva_outcome = models.CharField(
        max_length=250,
        choices=VIVA_OUTCOMES,
        default='Apt',
        blank=True,
    )

    held_at_university = models.ForeignKey(
        'organizations.Organization',
        blank=True,
        null=True,
    )

    phd_program = models.ForeignKey(
        'utils.PhDProgram',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['slug']
        verbose_name = u'Thesis'
        verbose_name_plural = u'Theses'

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title.encode('utf-8')))
        super(Thesis, self).save(*args, **kwargs)


###########################################################################
# Model: ThesisSeeAlso
###########################################################################

class ThesisSeeAlso(BaseModel):
    thesis = models.ForeignKey('Thesis')

    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.thesis.title, self.see_also)


###########################################################################
# Model: ThesisAbstract
###########################################################################

class ThesisAbstract(BaseModel):
    thesis = models.ForeignKey('Thesis')
    language = models.ForeignKey('utils.Language')

    abstract = RedactorField(
        max_length=5000,
        blank=True,
    )

    class Meta:
        verbose_name = u'Thesis abstract'
        verbose_name_plural = u'Thesis abstracts'

    def __unicode__(self):
        return u'Abstract in %s for: %s' % (self.language.name, self.thesis.title)


###########################################################################
# Model: CoAdvisor
###########################################################################

class CoAdvisor(BaseModel):
    thesis = models.ForeignKey('Thesis')
    co_advisor = models.ForeignKey('persons.Person')

    class Meta:
        verbose_name = u'Co-advisor'
        verbose_name_plural = u'Co-advisors'

    def __unicode__(self):
        return u'%s has co-advised the thesis: %s' % (self.co_advisor.full_name, self.thesis.title)


###########################################################################
# Model: VivaPanel
###########################################################################

class VivaPanel(BaseModel):
    thesis = models.ForeignKey('Thesis')

    person = models.ForeignKey('persons.Person')

    role = models.CharField(
        max_length=150,
        choices=VIVA_PANEL_ROLES,
    )

    class Meta:
        verbose_name = u'VIVA panel'
        verbose_name_plural = u'VIVA panels'


###########################################################################
# Model: Ranking
###########################################################################

class Ranking(BaseModel):
    name = models.CharField(
        max_length=50,
    )

    slug = models.SlugField(
        max_length=50,
        blank=True,
        unique=True,
    )

    icon = models.ImageField(
        upload_to=ranking_icon_picture_path,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = u'Ranking'
        verbose_name_plural = u'Rankings'

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(Ranking, self).save(*args, **kwargs)


###########################################################################
# Model: PublicationRank
###########################################################################

class PublicationRank(BaseModel):
    publication = models.ForeignKey('Publication')

    ranking = models.ForeignKey('Ranking')

    class Meta:
        verbose_name = u'Publication ranking'
        verbose_name_plural = u'Publication rankings'
