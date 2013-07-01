from django.db import models

from entities.publications.models import Publication

class ZoteroLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    zotero_key = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )
    attachment = models.BooleanField(default=False)
    publication = models.ForeignKey(Publication)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.created, self.zotero_key, self.publication.id)