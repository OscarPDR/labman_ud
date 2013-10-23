# coding: utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags

from ckeditor.fields import RichTextField


# Create your models here.


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


#########################
# Model: Person
#########################

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

    biography = RichTextField(blank=True, null=True)

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

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def save(self, *args, **kwargs):
        full_name = self.first_name + ' ' + self.first_surname

        if self.second_surname:
            full_name = full_name + ' ' + self.second_surname

        self.full_name = full_name

        self.slug = slugify(self.full_name)

        safe_biography = strip_tags(self.biography)
        safe_biography = safe_biography.replace("&lsquo;", "'")
        safe_biography = safe_biography.replace("&rsquo;", "'")
        safe_biography = safe_biography.replace("&ldquo;", "\"")
        safe_biography = safe_biography.replace("&rdquo;", "\"")
        self.safe_biography = safe_biography

        super(Person, self).save(*args, **kwargs)


#########################
# Model: AccountProfile
#########################

class AccountProfile(models.Model):
    person = models.ForeignKey('Person')

    network = models.ForeignKey('utils.Network')

    profile_id = models.CharField(
        max_length=150,
    )

    def __unicode__(self):
        return u'%s\'s %s account profile: %s' % (self.person.full_name, self.network.name, self.profile_id)


#########################
# Model: Nickname
#########################

class Nickname(models.Model):
    person = models.ForeignKey('Person')

    nickname = models.CharField(
        max_length=150,
    )

    class Meta:
        ordering = ['nickname']

    def __unicode__(self):
        return u'%s is also known as: %s' % (self.person.first_name, self.nickname)


#########################
# Model: Job
#########################

class Job(models.Model):
    person = models.ForeignKey('Person')

    position = models.CharField(
        max_length=250,
        blank=True,
    )

    description = models.TextField(
        max_length=2500,
        blank=True,
    )

    organization = models.ForeignKey('organizations.Organization')

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


#########################
# Model: PhDProgramFollowedByPerson
#########################

class PhDProgramFollowedByPerson(models.Model):
    person = models.ForeignKey('Person')
    phd_program = models.ForeignKey('utils.PhDProgram')


#########################
# Model: ThesisRegisteredByPerson
#########################

class ThesisRegisteredByPerson(models.Model):
    person = models.ForeignKey('Person')
    thesis = models.ForeignKey('publications.Thesis')
