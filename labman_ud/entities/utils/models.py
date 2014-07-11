# -*- encoding: utf-8 -*-

import os

from django.db import models
from django.template.defaultfilters import slugify
from entities.core.models import BaseModel

from redactor.fields import RedactorField
from .linked_data import *

# Create your models here.


def network_icon_path(self, filename):
    return "%s/%s%s" % ("networks", self.slug, os.path.splitext(filename)[-1])


def file_path(self, filename):
    return "%s/%s%s" % ("files", self.slug, os.path.splitext(filename)[-1])


###########################################################################
# Model: City
###########################################################################

class City(BaseModel):
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

    country = models.ForeignKey(
        'Country',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name.encode('utf-8')

        self.slug = slugify(self.short_name)

        super(City, self).save(*args, **kwargs)


###########################################################################
# Model: Country
###########################################################################

class Country(BaseModel):
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
        delete_country_rdf(self)

        if not self.short_name:
            self.short_name = self.full_name.encode('utf-8')

        self.slug = slugify(self.short_name)

        super(Country, self).save(*args, **kwargs)

        save_country_as_rdf(self)


###########################################################################
# Model: GeographicalScope
###########################################################################

class GeographicalScope(BaseModel):
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
        delete_geographical_scope_rdf(self)

        self.slug = slugify(str(self.name))
        super(GeographicalScope, self).save(*args, **kwargs)

        save_geographical_scope_as_rdf(self)


###########################################################################
# Model: Role
###########################################################################

class Role(BaseModel):
    name = models.CharField(
        max_length=100,
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
        self.slug = slugify(str(self.name))
        super(Role, self).save(*args, **kwargs)


###########################################################################
# Model: Tag
###########################################################################

class Tag(BaseModel):
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
        delete_tag_rdf(self)

        self.slug = slugify(str(self.name))
        super(Tag, self).save(*args, **kwargs)

        save_tag_as_rdf(self)


###########################################################################
# Model: Language
###########################################################################

class Language(BaseModel):
    name = models.CharField(
        max_length=50,
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
# Model: Network
###########################################################################

class Network(BaseModel):
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
# Model: PhDProgram
###########################################################################

class PhDProgram(BaseModel):
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


###########################################################################
# Model: ContributionType
###########################################################################

class ContributionType(BaseModel):
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

class Contribution(BaseModel):
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
# Model: PersonRelatedToContribution
###########################################################################

class PersonRelatedToContribution(BaseModel):
    person = models.ForeignKey('persons.Person')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.person.full_name, self.contribution.title)


###########################################################################
# Model: ProjectRelatedToContribution
###########################################################################

class ProjectRelatedToContribution(BaseModel):
    project = models.ForeignKey('projects.Project')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.project.full_name, self.contribution.title)


###########################################################################
# Model: PublicationRelatedToContribution
###########################################################################

class PublicationRelatedToContribution(BaseModel):
    publication = models.ForeignKey('publications.Publication')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.publication.title, self.contribution.title)


###########################################################################
# Model: TagRelatedToContribution
###########################################################################

class TagRelatedToContribution(BaseModel):
    tag = models.ForeignKey('Tag')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.tag.name, self.contribution.title)


###########################################################################
# Model: FileItemRelatedToContribution
###########################################################################

class FileItemRelatedToContribution(BaseModel):
    file_item = models.ForeignKey('FileItem')
    contribution = models.ForeignKey('Contribution')

    def __unicode__(self):
        return u'%s related contribution:%s' % (self.file_item.name, self.contribution.title)


###########################################################################
# Model: FileItem
###########################################################################

class FileItem(BaseModel):
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

class License(BaseModel):
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
# Model: TalkOrCourse
###########################################################################

class TalkOrCourse(BaseModel):
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
# Model: PersonRelatedToTalkOrCourse
###########################################################################

class PersonRelatedToTalkOrCourse(BaseModel):
    person = models.ForeignKey('persons.Person')
    talk_or_course = models.ForeignKey('TalkOrCourse')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.person.full_name, self.talk_or_course.title)


###########################################################################
# Model: ProjectRelatedToTalkOrCourse
###########################################################################

class ProjectRelatedToTalkOrCourse(BaseModel):
    project = models.ForeignKey('projects.Project')
    talk_or_course = models.ForeignKey('TalkOrCourse')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.project.full_name, self.talk_or_course.title)


###########################################################################
# Model: TagRelatedToTalkOrCourse
###########################################################################

class TagRelatedToTalkOrCourse(BaseModel):
    tag = models.ForeignKey('Tag')
    talk_or_course = models.ForeignKey('TalkOrCourse')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.tag.name, self.talk_or_course.title)


###########################################################################
# Model: FileItemRelatedToTalkOrCourse
###########################################################################

class FileItemRelatedToTalkOrCourse(BaseModel):
    file_item = models.ForeignKey('FileItem')
    talk_or_course = models.ForeignKey('TalkOrCourse')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.file_item.name, self.talk_or_course.title)


###########################################################################
# Model: Award
###########################################################################

class Award(BaseModel):
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
# Model: PersonRelatedToAward
###########################################################################

class PersonRelatedToAward(BaseModel):
    person = models.ForeignKey('persons.Person')
    award = models.ForeignKey('Award')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.person.full_name, self.award.full_name)


###########################################################################
# Model: ProjectRelatedToAward
###########################################################################

class ProjectRelatedToAward(BaseModel):
    project = models.ForeignKey('projects.Project')
    award = models.ForeignKey('Award')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.project.full_name, self.award.full_name)


###########################################################################
# Model: PublicationRelatedToAward
###########################################################################

class PublicationRelatedToAward(BaseModel):
    publication = models.ForeignKey('publications.Publication')
    award = models.ForeignKey('Award')

    def __unicode__(self):
        return u'%s related talk or course:%s' % (self.publication.title, self.award.full_name)
