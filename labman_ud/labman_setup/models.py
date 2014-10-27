
from django.db import models
from redactor.fields import RedactorField
from django.template.defaultfilters import slugify

import os


# Create your models here.


def team_picture_path(self, filename):
    return "%s/%s%s" % ('research_group', 'team', os.path.splitext(filename)[-1])


def official_logo_picture_path(self, filename):
    return "%s/%s%s" % ('research_group', 'official_logo', os.path.splitext(filename)[-1])


def official_network_picture_path(self, filename):
    return "%s/%s/%s%s" % ('research_group', 'social_profiles', self.slug, os.path.splitext(filename)[-1])


def favicon_picture_path(self, filename):
    return "%s/%s%s" % ('research_group', 'favicon', os.path.splitext(filename)[-1])


####################################################################################################
###     Model: LabmanDeployGeneralSettings
####################################################################################################

class LabmanDeployGeneralSettings(models.Model):

    base_url = models.URLField(
        blank=True,
        null=True,
    )

    favicon = models.ImageField(
        upload_to=favicon_picture_path,
        blank=True,
        null=True,
    )

    research_group_full_name = models.CharField(
        max_length=75,
    )

    research_group_short_name = models.CharField(
        max_length=75,
        blank=True,
        null=True,
    )

    research_group_team_image = models.ImageField(
        upload_to=team_picture_path,
        blank=True,
        null=True,
    )

    research_group_official_logo = models.ImageField(
        upload_to=official_logo_picture_path,
        blank=True,
        null=True,
    )

    research_group_description = RedactorField()

    # Address details
    address = RedactorField(
        blank=True,
        null=True,
    )

    map_external_link = models.URLField(
        blank=True,
        null=True,
    )

    # Contact details
    phone_number = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )

    phone_extension = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )

    email_address = models.EmailField(
        blank=True,
        null=True,
    )

    contact_person = models.CharField(
        max_length=75,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.research_group_short_name:
            self.research_group_short_name = self.research_group_full_name

        super(LabmanDeployGeneralSettings, self).save(*args, **kwargs)


####################################################################################################
###     Model: OfficialSocialProfile
####################################################################################################

class OfficialSocialProfile(models.Model):

    network_image = models.ImageField(
        upload_to=official_network_picture_path,
    )

    profile_link = models.URLField()

    name = models.CharField(
        max_length=50,
    )

    slug = models.CharField(
        max_length=50,
        blank=True,
    )

    help_text = models.CharField(
        max_length=75,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.encode('utf-8'))

        super(OfficialSocialProfile, self).save(*args, **kwargs)


####################################################################################################
###     Model: TweetPonyConfiguration
####################################################################################################

class TweetPonyConfiguration(models.Model):

    consumer_key = models.CharField(
        max_length=100,
    )

    consumer_secret = models.CharField(
        max_length=100,
    )

    access_token = models.CharField(
        max_length=100,
    )

    access_token_secret = models.CharField(
        max_length=100,
    )

    http_proxy = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    https_proxy = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    karmacracy_username = models.CharField(
        max_length=75,
        blank=True,
        null=True,
    )

    karmacracy_api_key = models.CharField(
        max_length=75,
        blank=True,
        null=True,
    )


####################################################################################################
###     Model: ZoteroConfiguration
####################################################################################################

class ZoteroConfiguration(models.Model):

    consumer_key = models.CharField(
        max_length=100,
    )

    api_key = models.CharField(
        max_length=100,
    )

    library_id = models.CharField(
        max_length=100,
    )

    library_type = models.CharField(
        max_length=100,
    )


####################################################################################################
###     Model: SEOAndAnalytics
####################################################################################################

class SEOAndAnalytics(models.Model):

    meta_keywords = models.TextField(
        max_length=750,
        blank=True,
        null=True,
    )

    meta_description = models.TextField(
        max_length=750,
        blank=True,
        null=True,
    )

    google_analytics_account = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
