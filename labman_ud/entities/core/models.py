
from django.db import models
from datetime import datetime


class BaseModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified'
    """

    log_created = models.DateTimeField(
        auto_now_add=True,
        default=datetime.today(),
    )

    log_modified = models.DateTimeField(
        auto_now=True,
        default=datetime.today(),
    )

    class Meta:
        abstract = True
