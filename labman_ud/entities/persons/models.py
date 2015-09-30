# -*- encoding: utf-8 -*-

import os

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags

from .linked_data import *

from redactor.fields import RedactorField


def person_profile_picture_path(self, filename):
    return "%s/%s%s" % ("persons", self.slug, os.path.splitext(filename)[-1])


def person_profile_konami_code_picture_path(self, filename):
    return "%s/%s%s" % ("konami_code_persons", self.slug, os.path.splitext(filename)[-1])


GENDERS = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

TITLES = (
    ('Dr.', 'Dr.'),
)


###     Person()
####################################################################################################

class Person(models.Model):
    first_name = models.CharField(
        max_length=25,
    )

    first_surname = models.CharField(
        max_length=50,
    )

    second_surname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    full_name = models.CharField(
        max_length=150,
        blank=True,
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
    )

    biography = RedactorField(blank=True, null=True)

    safe_biography = models.TextField(
        max_length=2500,
        blank=True,
    )

    title = models.CharField(
        max_length=15,
        choices=TITLES,
        blank=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDERS,
        blank=True,
    )

    personal_website = models.URLField(
        max_length=250,
        blank=True,
    )

    email = models.EmailField(
        max_length=150,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=25,
        blank=True,
    )

    phone_extension = models.CharField(
        max_length=10,
        blank=True,
    )

    # interests

    is_active = models.BooleanField(
        default=False,
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
        unique=True,
    )

    profile_picture = models.ImageField(
        upload_to=person_profile_picture_path,
        blank=True,
        null=True,
    )

    profile_konami_code_picture = models.ImageField(
        upload_to=person_profile_konami_code_picture_path,
        blank=True,
        null=True,
    )

    konami_code_position = models.CharField(
        max_length=150,
        blank=True,
    )

    publications = models.ManyToManyField('publications.Publication', through='publications.PublicationAuthor')
    projects = models.ManyToManyField('projects.Project', through='projects.AssignedPerson')

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def email_user(self):
        if not self.email or '@' not in self.email:
            return self.email
        else:
            return self.email.split('@')[0]

    def email_domain(self):
        if not self.email or '@' not in self.email:
            return self.email
        else:
            return self.email.split('@')[1]

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            old_slug = self.slug
            delete_person_rdf(self)

        full_name = self.first_name + ' ' + self.first_surname

        if self.second_surname:
            full_name = full_name + ' ' + self.second_surname

        self.full_name = full_name

        self.slug = slugify(self.full_name)

        try:
            safe_biography = strip_tags(self.biography)
            safe_biography = safe_biography.replace("&lsquo;", "'")
            safe_biography = safe_biography.replace("&rsquo;", "'")
            safe_biography = safe_biography.replace("&ldquo;", "\"")
            safe_biography = safe_biography.replace("&rdquo;", "\"")
        except:
            safe_biography = ''

        self.safe_biography = safe_biography

        super(Person, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            for see_also in self.see_also_links.all():
                see_also.save()

            # To avoid triple deletion, generate triples for related Job instances
            for job in self.job_set.all():
                job.save()

            # To avoid triple deletion, generate triples for related AccountProfile instances
            for account_profile in self.accountprofile_set.all():
                account_profile.save()

            save_person_as_rdf(self)
            update_person_object_triples(old_slug, self.slug)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_person_rdf(self)

        super(Person, self).delete(*args, **kwargs)


###     PersonSeeAlso()
####################################################################################################

class PersonSeeAlso(models.Model):
    person = models.ForeignKey('Person', related_name='see_also_links')

    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.person.full_name, self.see_also)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_person_see_also_rdf(self)

        super(PersonSeeAlso, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_person_see_also_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_person_see_also_rdf(self)

        super(PersonSeeAlso, self).delete(*args, **kwargs)


###     AccountProfile()
####################################################################################################

class AccountProfile(models.Model):
    person = models.ForeignKey('Person')

    network = models.ForeignKey('utils.Network')

    profile_id = models.CharField(
        max_length=150,
    )

    # def __unicode__(self):
    #     return u'%s\'s %s account profile: %s' % (self.person.full_name, self.network.name, self.profile_id)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_account_profile_rdf(self)

        super(AccountProfile, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_account_profile_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_account_profile_rdf(self)

        super(AccountProfile, self).delete(*args, **kwargs)


###     Nickname()
####################################################################################################

class Nickname(models.Model):
    person = models.ForeignKey('Person', related_name='nicknames')

    nickname = models.CharField(
        max_length=150,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
        #unique=True,
    )

    class Meta:
        ordering = ['nickname']

    def __unicode__(self):
        return u'%s is also known as: %s' % (self.person.first_name, self.nickname)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_nickname_rdf(self)

        self.slug = slugify(self.nickname)
        super(Nickname, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_nickname_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_nickname_rdf(self)

        super(Nickname, self).delete(*args, **kwargs)


###     Job()
####################################################################################################

class Job(models.Model):
    person = models.ForeignKey('Person')
    organization = models.ForeignKey('organizations.Organization')

    position = models.CharField(
        max_length=250,
        blank=True,
    )

    description = models.TextField(
        max_length=2500,
        blank=True,
    )

    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s worked as %s at %s' % (self.person.full_name, self.position, self.organization.short_name)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_job_rdf(self)

        super(Job, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_job_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_job_rdf(self)

        super(Job, self).delete(*args, **kwargs)


###     PhDProgramFollowedByPerson()
####################################################################################################

class PhDProgramFollowedByPerson(models.Model):
    person = models.ForeignKey('Person')
    phd_program = models.ForeignKey('utils.PhDProgram')


###     ThesisRegisteredByPerson()
####################################################################################################

class ThesisRegisteredByPerson(models.Model):
    person = models.ForeignKey('Person')
    thesis = models.ForeignKey('publications.Thesis')
