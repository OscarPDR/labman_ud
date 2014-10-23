
from django.db import models
from entities.core.models import BaseModel


# Create your models here.


###########################################################################
# Model: IgnoredSimilarNames
###########################################################################

class IgnoredSimilarNames(BaseModel):
    test_person = models.ForeignKey('persons.Person', related_name='test_person')

    testing_person = models.ForeignKey('persons.Person', related_name='testing_person')
