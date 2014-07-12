# -*- encoding: utf-8 -*-

import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from entities.core.models import BaseModel

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


def publication_path(self, filename):
    publication_type_slug = slugify(self.child_type)

    sub_folder = publication_type_slug

    try:
        sub_folder = '%s/%s' % (sub_folder, self.presented_at.slug)
    except:
        pass

    return "%s/%s/%s/%s%s" % ("publications", self.published.year, sub_folder, self.slug, os.path.splitext(filename)[-1])


def thesis_path(self, filename):
    return "%s/%s/%s%s" % ("publications", "theses", self.slug, os.path.splitext(filename)[-1])


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

    authors = models.ManyToManyField('persons.Person', through='PublicationAuthor')
    tags = models.ManyToManyField('utils.Tag', through='PublicationTag')

    class Meta:
        # abstract = True
        ordering = ['-slug']

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
        self.slug = slugify(str(self.title.encode('utf-8')))

        if self.child_type == '':
            self.child_type = self.__class__.__name__

        super(Publication, self).save(*args, **kwargs)


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


###########################################################################
# Model: BookSection
###########################################################################

class BookSection(ISIDBLPTags):
    parent_book = models.ForeignKey('Book')

    presented_at = models.ForeignKey('events.Event', null=True, blank=True)

    core = models.CharField(
        max_length=25,
        choices=CORE_CHOICES,
        default='None',
        blank=True,
    )


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
        default='None',
        blank=True,
        null=True,
    )


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


###########################################################################
# Model: JournalArticle
###########################################################################

class JournalArticle(ISIDBLPTags):
    parent_journal = models.ForeignKey('Journal')

    individually_published = models.DateField(
        blank=True,
        null=True,
    )


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


###########################################################################
# Model: MagazineArticle
###########################################################################

class MagazineArticle(PartOfCollectionPublication):
    parent_magazine = models.ForeignKey('Magazine')


###########################################################################
# Model: PublicationTag
###########################################################################

class PublicationTag(BaseModel):
    tag = models.ForeignKey('utils.Tag')
    publication = models.ForeignKey('publications.Publication')

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

    def __unicode__(self):
        return u'%s has written: %s as author #%d' % (self.author.full_name, self.publication.title, self.position)


###########################################################################
# Model: PublicationEditor
###########################################################################

class PublicationEditor(BaseModel):
    editor = models.ForeignKey('persons.Person')
    publication = models.ForeignKey('publications.Publication')

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

    viva = models.ForeignKey('events.Viva')

    phd_program = models.ForeignKey('utils.PhDProgram')

    class Meta:
        ordering = ['slug']

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

    abstract = models.TextField(
        max_length=5000,
        blank=True,
    )

    def __unicode__(self):
        return u'Abstract in %s for: %s' % (self.language.name, self.thesis.title)


###########################################################################
# Model: CoAdvisor
###########################################################################

class CoAdvisor(BaseModel):
    thesis = models.ForeignKey('Thesis')
    co_advisor = models.ForeignKey('persons.Person')

    def __unicode__(self):
        return u'%s has co-advised the thesis: %s' % (self.co_advisor.full_name, self.thesis.title)
