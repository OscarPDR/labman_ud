# coding=utf-8

import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from redactor.fields import RedactorField

from .linked_data import *


def project_logo_path(self, filename):
    return "%s/%s%s" % ("projects", self.slug, os.path.splitext(filename)[-1])


MIN_YEAR_LIMIT = 1950
MAX_YEAR_LIMIT = 2080


PROJECT_STATUS = (
    ('Not started', 'Not started'),
    ('Ongoing', 'Ongoing'),
    ('Finished', 'Finished'),
)

MONTHS = (
    ('01', 'January'),
    ('02', 'February'),
    ('03', 'March'),
    ('04', 'April'),
    ('05', 'May'),
    ('06', 'June'),
    ('07', 'July'),
    ('08', 'August'),
    ('09', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)

PROJECT_TYPES = (
    ('Applied research project', 'Applied research project'),
    ('Development project', 'Development project'),
    ('External project', 'External project'),
    ('Innovation project', 'Innovation project'),
    ('Internal project', 'Internal project'),
    ('Project', 'Project'),
    ('Research contract', 'Research contract'),
    ('Research project', 'Research project'),
)


###########################################################################
# Model: Project
###########################################################################

class Project(models.Model):
    project_leader = models.ForeignKey('organizations.Organization')

    project_type = models.CharField(
        max_length=50,
        choices=PROJECT_TYPES,
        default='Project',
    )

    full_name = models.CharField(
        max_length=250,
    )

    short_name = models.CharField(
        max_length=250,
        blank=True,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
    )

    description = RedactorField(
        max_length=3000,
        blank=True,
        null=True,
    )

    homepage = models.URLField(
        max_length=150,
        blank=True,
        null=True,
    )

    start_month = models.CharField(
        max_length=25,
        choices=MONTHS,
        default='01',
    )

    start_year = models.IntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
    )

    end_month = models.CharField(
        max_length=25,
        choices=MONTHS,
        default='12',
    )

    end_year = models.IntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
    )

    status = models.CharField(
        max_length=25,
        choices=PROJECT_STATUS,
        default='Not started',
    )

    observations = models.TextField(
        max_length=1000,
        blank=True,
    )

    logo = models.ImageField(
        upload_to=project_logo_path,
        blank=True,
        null=True,
    )

    private_funding_details = models.BooleanField(default=False)

    assigned_people = models.ManyToManyField('persons.Person', through='AssignedPerson', related_name='assigned_projects')
    consortium_members = models.ManyToManyField('organizations.Organization', through='ConsortiumMember', related_name='consortium_member_of')
    related_publications = models.ManyToManyField('publications.Publication', through='RelatedPublication', related_name='related_projects')
    tags = models.ManyToManyField('utils.Tag', through='ProjectTag', related_name='projects')

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def save(self, *args, **kwargs):
        old_slug = self.slug

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_project_rdf(self)

        if not self.short_name:
            self.short_name = self.full_name.encode('utf-8')

        self.description = self.description.replace("<img src=", "<img class='img-responsive' src=")

        self.slug = slugify(self.short_name.encode('utf-8'))
        super(Project, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_project_as_rdf(self)
            update_project_object_triples(old_slug, self.slug)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_project_rdf(self)

        super(Project, self).delete(*args, **kwargs)


###########################################################################
# Model: ProjectSeeAlso
###########################################################################

class ProjectSeeAlso(models.Model):
    project = models.ForeignKey('Project')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.project.full_name, self.see_also)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_project_see_also_rdf(self)

        super(ProjectSeeAlso, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_project_see_also_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_project_see_also_rdf(self)

        super(ProjectSeeAlso, self).delete(*args, **kwargs)


###########################################################################
# Model: Funding
###########################################################################

class Funding(models.Model):
    project = models.ForeignKey('Project')

    funding_program = models.ForeignKey('funding_programs.FundingProgram')

    project_code = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    total_funds = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        max_length=500,
        blank=True,
    )

    def __unicode__(self):
        return u'%s funded by %s - Project code: %s' % (self.project.short_name, self.funding_program.short_name, self.project_code)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_funding_rdf(self)

        if not self.project_code:
            self.slug = self.project.slug + '_' + self.funding_program.slug
        else:
            self.slug = slugify(str(self.project_code))

        super(Funding, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_funding_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_funding_rdf(self)

        super(Funding, self).delete(*args, **kwargs)


###########################################################################
# Model: FundingSeeAlso
###########################################################################

class FundingSeeAlso(models.Model):
    funding = models.ForeignKey('Funding')

    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.funding.slug, self.see_also)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_funding_see_also_rdf(self)

        super(FundingSeeAlso, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_funding_see_also_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_funding_see_also_rdf(self)

        super(FundingSeeAlso, self).delete(*args, **kwargs)


###########################################################################
# Model: FundingAmount
###########################################################################

class FundingAmount(models.Model):
    funding = models.ForeignKey('Funding')

    own_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    year = models.IntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
    )

    def __unicode__(self):
        return u'Year %s - %s € (own amount)' % (self.year, self.own_amount)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_funding_amount_rdf(self)

        super(FundingAmount, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_funding_amount_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_funding_amount_rdf(self)

        super(FundingAmount, self).delete(*args, **kwargs)


###########################################################################
# Model: AssignedPerson
###########################################################################

class AssignedPerson(models.Model):
    project = models.ForeignKey('Project')

    person = models.ForeignKey('persons.Person')

    role = models.ForeignKey('utils.Role')

    start_date = models.DateField(
        blank=True,
        null=True
    )

    end_date = models.DateField(
        blank=True,
        null=True
    )

    description = models.TextField(
        max_length=1500,
        blank=True
    )

    tags = models.ManyToManyField('utils.Tag', through='AssignedPersonTag', related_name='assigned_persons')

    def __unicode__(self):
        return u'%s is working at %s as a %s' % (self.person.full_name, self.project.short_name, self.role.name)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_assigned_person_rdf(self)

        super(AssignedPerson, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_assigned_person_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_assigned_person_rdf(self)

        super(AssignedPerson, self).delete(*args, **kwargs)


###########################################################################
# Model: AssignedPersonTag
###########################################################################

class AssignedPersonTag(models.Model):
    tag = models.ForeignKey('utils.Tag')
    assigned_person = models.ForeignKey('AssignedPerson')

    def __unicode__(self):
        return u'%s tagged as: %s' % (self.assigned_person.person, self.tag.name)


###########################################################################
# Model: ConsortiumMember
###########################################################################

class ConsortiumMember(models.Model):
    project = models.ForeignKey('Project')

    organization = models.ForeignKey('organizations.Organization')

    def __unicode__(self):
        return u'%s is taking part in %s' % (self.organization.short_name, self.project.short_name)


###########################################################################
# Model: ProjectTag
###########################################################################

class ProjectTag(models.Model):
    tag = models.ForeignKey('utils.Tag')
    project = models.ForeignKey('Project')

    def __unicode__(self):
        return u'%s tagged as: %s' % (self.project.full_name, self.tag.name)


###########################################################################
# Model: RelatedPublication
###########################################################################

class RelatedPublication(models.Model):
    project = models.ForeignKey('Project')
    publication = models.ForeignKey('publications.Publication', related_name='projects')

    def __unicode__(self):
        return u'Project: %s - Publication: %s' % (self.project.short_name, self.publication.title)
