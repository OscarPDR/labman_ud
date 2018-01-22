# -*- encoding: utf-8 -*-

import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from labman_ud.util import nslugify

# from .linked_data import *
from .choices import *

from redactor.fields import RedactorField


def dataset_path(self, filename):
    """
    Returns a path to be inserted into database which contains the logical path of the stored database in the
    webpage disk


    :param self:
    :param filename: the name of the dataset to be stored
    :return:
    """
    return "%s/%s/%s/%s%s" % ("datasets/data", self.date.year, self.format, self.slug, os.path.splitext(filename)[-1])


def dataset_logo_path(self, filename):
    """
    Returns a path to be inserted into database which contains the logical path of the stored logo of the dataset

    :param self:
    :param filename: the name of the dataset logo to be stored
    :return:
    """
    return "%s/%s/%s/%s%s" % ("datasets/logo", self.date.year, self.format, self.slug, os.path.splitext(filename)[-1])


###		Datasets
####################################################################################################

class Dataset(models.Model):
    # Table models

    # Dataset title
    title = models.CharField(
        max_length=250,
        blank=False,
        null=False,
        unique=True
    )
    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
    )
    # When we add the databaset into DB
    date = models.DateTimeField(
        auto_now_add=True
    )
    # The file path in the server
    file = models.FileField(
        max_length=1000,
        upload_to=dataset_path,
        blank=True,
        null=True,
    )
    # File type
    format = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=FILE_FORMAT_CHOICES,
        default='ext'
    )
    # Main page of the dataset's download page
    main_webpage = models.URLField(
        max_length=250,
        blank=True,
        null=True
    )
    # External download url from other server (url)
    external_download_url = models.URLField(
        max_length=250,
        blank=True,
        null=True
    )
    # Description of the dataset
    notes = models.TextField(
        max_length=25000,
        blank=False,
        null=False
    )
    # Where is the dataset logo stored (An image to recognize the dataset)
    # logo = models.ImageField(
    #     upload_to=dataset_logo_path,
    #     blank=True,
    #     null=True,
    # )
    # License (if available)
    license = models.CharField(
        max_length=50,
        blank=True,
        default='ne',
        choices=LICENSE_CHOICES,
    )
    # Current version of the dataset
    version = models.FloatField(
        default=1.0,
        blank=False,
        null=False
    )
    # Doi of the dataset --> http://doi.org/XXX
    doi = models.URLField(
        max_length=250,
        blank=True,
        null=True
    )

    # M2M field to util tag to store tags of this dataset
    tags = models.ManyToManyField('utils.Tag', through='DatasetTag')
    # M2M field to authors of the dataset
    authors = models.ManyToManyField('persons.Person', through='DatasetAuthor', related_name='dataset_authors')
    # M2M field to projects of the dataset
    projects = models.ManyToManyField('projects.Project', through='DatasetProject', related_name='dataset_projects')

    class Meta:
        # abstract = True
        ordering = ['-slug']
        verbose_name = u'Dataset'
        verbose_name_plural = u'Datasets'

    def clean(self):
        if self.external_download_url and self.file.name:
            # We have both, download url and file name, raising error
            raise ValidationError(u"You need to provide only one: internal file or External download link")
        elif self.file and self.file.name and len(self.file.name) > 0 and not self.external_download_url:
            # We have a valid file, check if the extension in correct.
            extension = os.path.splitext(self.file.name)[-1].split('.')[-1]
            # Checking extension againts the
            found = False
            for f_format in FILE_FORMAT_CHOICES:
                if extension in f_format[0]:
                    found = True
                    break
            if not found:
                raise ValidationError(u'The uploaded file contains an invalid dataset extension'
                                      u''
                                      u'Supported extensions:'
                                      u' '
                                      + ' '.join([value[1] for value in FILE_FORMAT_CHOICES]))
        elif not self.external_download_url and not self.file.name:
            # The user must provide at least something.
            raise ValidationError(u"Please, provide a internal dataset file or a external link")
        elif self.doi and not self.doi.startswith('http://doi.org/'):
            # The provided doi url is not valid
            raise ValidationError(u"Please, provide a valid DOI url in format: 'http://doi.org/XXXXX'")
        # The validation of the external_download_url is done by django

    def display_all_fields(self):
        all_fields = [
            self.title,
            self.slug,
        ]

        for author in self.authors.all():
            all_fields.append(author.full_name)

        for project in self.projects.all():
            all_fields.append(project.full_name)

        for tag in self.tags.all():
            all_fields.append(tag.name)

        return u' '.join([field for field in all_fields if field])

    def __unicode__(self):
        return u'%s' % self.title

    def _generate_slug(self):
        return slugify(self.title.encode('utf-8'))

    def save(self, *args, **kwargs):
        # Updating slug with the new name of the dataset
        old_slug = self.slug
        self.slug = self._generate_slug()

        if self.file.name:
            # giving the extension value based on file extension
            self.format = os.path.splitext(self.file.name)[-1][1:]
        else:
            # giving the extension value as a external link 'extension'
            self.format = "ext"

        super(Dataset, self).save(*args, **kwargs)

        # TODO finish when you have the lod fixed
        # Publish RDF data
        # if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
        #    save_publication_as_rdf(self)
        #    update_publication_object_triples(old_slug, self.slug)


###		DatasetTag
####################################################################################################

class DatasetTag(models.Model):
    tag = models.ForeignKey('utils.Tag')
    dataset = models.ForeignKey('datasets.Dataset')

    class Meta:
        verbose_name = u'Dataset tag'
        verbose_name_plural = u'Dataset tags'

    class Meta:
        ordering = ['tag__slug']

    def __unicode__(self):
        return u'%s tagged as: %s' % (self.dataset.title, self.tag.name)


###     DatasetProject
####################################################################################################

class DatasetProject(models.Model):
    project = models.ForeignKey('projects.Project')
    dataset = models.ForeignKey('datasets.Dataset')

    class Meta:
        verbose_name = u'Dataset project'
        verbose_name_plural = u'Dataset projects'

    def __unicode__(self):
        return u'%s is part of the %s project' % (self.dataset.title, self.project.full_name)


###		DatasetAuthor
####################################################################################################

class DatasetAuthor(models.Model):
    author = models.ForeignKey('persons.Person')
    dataset = models.ForeignKey('datasets.Dataset')

    position = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'Dataset author'
        verbose_name_plural = u'Dataset authors'

    def __unicode__(self):
        return u'%s has created: %s as author' % (self.dataset.title, self.author.full_name)
