from django.db import models


class ZoteroLog(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
    )

    zotero_key = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )

    updated = models.DateTimeField()

    delete = models.BooleanField(
        default=False,
    )

    version = models.PositiveIntegerField(
        blank=False,
        null=False,
    )

    observations = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    publication = models.ForeignKey(
        'publications.Publication',
        related_name='zotero_logs',
        default=None,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s | %s' % (self.version, self.zotero_key)
