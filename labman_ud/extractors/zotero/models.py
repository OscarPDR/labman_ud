# -*- encoding: utf-8 -*-

from django.db import models


###     ZoteroExtractorLog()
####################################################################################################

class ZoteroExtractorLog(models.Model):
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    item_key = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )

    version = models.PositiveIntegerField()

    publication = models.ForeignKey(
        'publications.Publication',
        related_name='zotero_extractor_logs',
        default=None,
        blank=True,
        null=True,
    )
