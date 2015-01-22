
from django.db import models


# Create your models here.


###########################################################################
# Model: IgnoredSimilarNames
###########################################################################

class IgnoredSimilarNames(models.Model):
    test_person = models.ForeignKey('persons.Person', related_name='test_person')

    testing_person = models.ForeignKey('persons.Person', related_name='testing_person')
