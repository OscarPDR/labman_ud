from django.db import models

from entities.publications.models import Publication

class ZoteroLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    zotero_key = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )
    updated = models.DateTimeField()
    attachment = models.BooleanField(default=False)
    version = models.PositiveIntegerField(
        blank=False,
        null=False,
    )
    observations = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    publication = models.ForeignKey(Publication)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.version, self.zotero_key, self.publication.id)