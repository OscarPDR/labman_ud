
import os

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

from redactor.fields import RedactorField
from .linked_data import *


def network_icon_path(self, filename):
    return "%s/%s%s" % ("networks", self.slug, os.path.splitext(filename)[-1])


def file_path(self, filename):
    return "%s/%s%s" % ("files", self.slug, os.path.splitext(filename)[-1])


###########################################################################
# Model: City
###########################################################################

class City(models.Model):
    full_name = models.CharField(
        max_length=150,
    )

    short_name = models.CharField(
        max_length=150,
        blank=True,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
    )

    latitude = models.FloatField(
        blank=True,
        null=True,
    )

    longitude = models.FloatField(
        blank=True,
        null=True,
    )

    country = models.ForeignKey(
        'Country',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        city_name = self.full_name

        if self.country:
            city_name = '%s (%s)' % (city_name, self.country.full_name)

        return u'%s' % (city_name)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name.encode('utf-8')

        self.slug = slugify(self.short_name)

        super(City, self).save(*args, **kwargs)


###########################################################################
# Model: CitySeeAlso
###########################################################################

class CitySeeAlso(models.Model):
    city = models.ForeignKey('City')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.city.full_name, self.see_also)


###########################################################################
# Model: Country
###########################################################################

class Country(models.Model):
    full_name = models.CharField(
        max_length=150,
    )

    short_name = models.CharField(
        max_length=150,
        blank=True,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_country_rdf(self)

        if not self.short_name:
            self.short_name = self.full_name.encode('utf-8')

        self.slug = slugify(self.short_name)

        super(Country, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_country_as_rdf(self)


###########################################################################
# Model: CountrySeeAlso
###########################################################################

class CountrySeeAlso(models.Model):
    country = models.ForeignKey('Country')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.country.full_name, self.see_also)


###########################################################################
# Model: GeographicalScope
###########################################################################

class GeographicalScope(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=u'Name',
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_geographical_scope_rdf(self)

        self.slug = slugify(str(self.name))
        super(GeographicalScope, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_geographical_scope_as_rdf(self)


###########################################################################
# Model: GeographicalScopeSeeAlso
###########################################################################

class GeographicalScopeSeeAlso(models.Model):
    geographical_scope = models.ForeignKey('GeographicalScope')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.geographical_scope.name, self.see_also)


###########################################################################
# Model: Role
###########################################################################

class Role(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    exclude_from_charts = models.BooleanField(
        default=False,
    )

    relevance_order = models.PositiveSmallIntegerField(
        default=0,
    )

    rgb_color = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name=u'RGB color (#)'
    )

    class Meta:
        ordering = ['relevance_order']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super(Role, self).save(*args, **kwargs)


###########################################################################
# Model: Tag
###########################################################################

class Tag(models.Model):
    name = models.CharField(
        max_length=75,
    )

    slug = models.SlugField(
        max_length=75,
        blank=True,
        unique=True,
    )

    sub_tag_of = models.ForeignKey(
        'self',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        name = self.name
        if self.sub_tag_of:
            name = name + ' < ' + self.sub_tag_of.name

        return u'%s' % (name)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_tag_rdf(self)

        self.slug = slugify(str(self.name))
        super(Tag, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_tag_as_rdf(self)


###########################################################################
# Model: TagSeeAlso
###########################################################################

class TagSeeAlso(models.Model):
    tag = models.ForeignKey('Tag')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.tag.name, self.see_also)


###########################################################################
# Model: Language
###########################################################################

class Language(models.Model):
    name = models.CharField(
        max_length=50,
    )

    language_tag = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        max_length=50,
        blank=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(Language, self).save(*args, **kwargs)


###########################################################################
# Model: LanguageSeeAlso
###########################################################################

class LanguageSeeAlso(models.Model):
    language = models.ForeignKey('Language')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.language.name, self.see_also)


###########################################################################
# Model: Network
###########################################################################

class Network(models.Model):
    name = models.CharField(
        max_length=150,
    )

    base_url = models.URLField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
    )

    # recommended size: 64*64 px
    # recommended format: .png
    icon = models.ImageField(
        upload_to=network_icon_path,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(Network, self).save(*args, **kwargs)


###########################################################################
# Model: NetworkSeeAlso
###########################################################################

class NetworkSeeAlso(models.Model):
    network = models.ForeignKey('Network')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.network.name, self.see_also)


###########################################################################
# Model: PhDProgram
###########################################################################

class PhDProgram(models.Model):
    name = models.CharField(
        max_length=500,
    )

    university = models.ForeignKey(
        'organizations.Organization',
        related_name='university_holding_a_phd_program',
    )

    faculty = models.ForeignKey(
        'organizations.Organization',
        related_name='faculty_holding_a_phd_program',
        blank=True,
    )

    homepage = models.URLField(
        max_length=250,
    )

    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'PhD program'
        verbose_name_plural = 'PhD programs'

    def __unicode__(self):
        return u'%s' % (self.name)


###########################################################################
# Model: PhDProgramSeeAlso
###########################################################################

class PhDProgramSeeAlso(models.Model):
    phd_program = models.ForeignKey('PhDProgram')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.phd_program.name, self.see_also)


###########################################################################
# Model: ContributionType
###########################################################################

class ContributionType(models.Model):
    name = models.CharField(
        max_length=100,
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
        unique=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(ContributionType, self).save(*args, **kwargs)


###########################################################################
# Model: Contribution
###########################################################################

class Contribution(models.Model):
    title = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        null=True,
    )

    contribution_type = models.ForeignKey('ContributionType')

    description = RedactorField()

    license = models.ForeignKey(
        'License',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(Contribution, self).save(*args, **kwargs)


###########################################################################
# Model: ContributionSeeAlso
###########################################################################

class ContributionSeeAlso(models.Model):
    contribution = models.ForeignKey('Contribution')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.contribution.title, self.see_also)


###########################################################################
# Model: PersonRelatedToContribution
###########################################################################

class PersonRelatedToContribution(models.Model):
    person = models.ForeignKey('persons.Person')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.person.full_name, self.contribution.title)


###########################################################################
# Model: ProjectRelatedToContribution
###########################################################################

class ProjectRelatedToContribution(models.Model):
    project = models.ForeignKey('projects.Project')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.project.full_name, self.contribution.title)


###########################################################################
# Model: PublicationRelatedToContribution
###########################################################################

class PublicationRelatedToContribution(models.Model):
    publication = models.ForeignKey('publications.Publication')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.publication.title, self.contribution.title)


###########################################################################
# Model: TagRelatedToContribution
###########################################################################

class TagRelatedToContribution(models.Model):
    tag = models.ForeignKey('Tag')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.tag.name, self.contribution.title)


###########################################################################
# Model: FileItemRelatedToContribution
###########################################################################

class FileItemRelatedToContribution(models.Model):
    file_item = models.ForeignKey('FileItem')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.file_item.name, self.contribution.title)


###########################################################################
# Model: FileItem
###########################################################################

class FileItem(models.Model):
    name = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        null=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    logo = models.FileField(
        upload_to=file_path,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(FileItem, self).save(*args, **kwargs)


###########################################################################
# Model: License
###########################################################################

class License(models.Model):
    full_name = models.CharField(
        max_length=150,
    )

    short_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
        null=True,
    )

    license_url = models.URLField()

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name

        self.slug = slugify(self.full_name)

        super(License, self).save(*args, **kwargs)


###########################################################################
# Model: LicenseSeeAlso
###########################################################################

class LicenseSeeAlso(models.Model):
    license = models.ForeignKey('License')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.license.full_name, self.see_also)


###########################################################################
# Model: TalkOrCourse
###########################################################################

class TalkOrCourse(models.Model):
    title = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        null=True,
    )

    description = RedactorField()

    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    event = models.ForeignKey(
        'events.Event',
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super(TalkOrCourse, self).save(*args, **kwargs)


###########################################################################
# Model: TalkOrCourseSeeAlso
###########################################################################

class TalkOrCourseSeeAlso(models.Model):
    talk_or_course = models.ForeignKey('TalkOrCourse')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.talk_or_course.title, self.see_also)


###########################################################################
# Model: PersonRelatedToTalkOrCourse
###########################################################################

class PersonRelatedToTalkOrCourse(models.Model):
    person = models.ForeignKey('persons.Person')
    talk_or_course = models.ForeignKey('TalkOrCourse')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.person.full_name, self.talk_or_course.title)


###########################################################################
# Model: ProjectRelatedToTalkOrCourse
###########################################################################

class ProjectRelatedToTalkOrCourse(models.Model):
    project = models.ForeignKey('projects.Project')
    talk_or_course = models.ForeignKey('TalkOrCourse')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.project.full_name, self.talk_or_course.title)


###########################################################################
# Model: TagRelatedToTalkOrCourse
###########################################################################

class TagRelatedToTalkOrCourse(models.Model):
    tag = models.ForeignKey('Tag')
    talk_or_course = models.ForeignKey('TalkOrCourse')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.tag.name, self.talk_or_course.title)


###########################################################################
# Model: FileItemRelatedToTalkOrCourse
###########################################################################

class FileItemRelatedToTalkOrCourse(models.Model):
    file_item = models.ForeignKey('FileItem')
    talk_or_course = models.ForeignKey('TalkOrCourse')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.file_item.name, self.talk_or_course.title)


###########################################################################
# Model: Award
###########################################################################

class Award(models.Model):
    full_name = models.CharField(
        max_length=250,
    )

    short_name = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        null=True,
    )

    description = RedactorField()

    date = models.DateField(
        blank=True,
        null=True,
    )

    event = models.ForeignKey(
        'events.Event',
        blank=True,
        null=True,
    )

    supporting_organization = models.ForeignKey(
        'organizations.Organization',
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name

        self.slug = slugify(self.full_name)

        super(Award, self).save(*args, **kwargs)


###########################################################################
# Model: AwardSeeAlso
###########################################################################

class AwardSeeAlso(models.Model):
    award = models.ForeignKey('Award')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.award.full_name, self.see_also)


###########################################################################
# Model: PersonRelatedToAward
###########################################################################

class PersonRelatedToAward(models.Model):
    person = models.ForeignKey('persons.Person')
    award = models.ForeignKey('Award')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.person.full_name, self.award.full_name)


###########################################################################
# Model: ProjectRelatedToAward
###########################################################################

class ProjectRelatedToAward(models.Model):
    project = models.ForeignKey('projects.Project')
    award = models.ForeignKey('Award')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.project.full_name, self.award.full_name)


###########################################################################
# Model: PublicationRelatedToAward
###########################################################################

class PublicationRelatedToAward(models.Model):
    publication = models.ForeignKey('publications.Publication')
    award = models.ForeignKey('Award')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.publication.title, self.award.full_name)
