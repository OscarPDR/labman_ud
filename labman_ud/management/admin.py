
from django.contrib import admin
from models import *


# Register your models here.


###########################################################################
# Class: IgnoredSimilarNamesAdmin
###########################################################################

class IgnoredSimilarNamesAdmin(admin.ModelAdmin):
    model = IgnoredSimilarNames

    list_display = ['test_person', 'testing_person']


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################

admin.site.register(IgnoredSimilarNames, IgnoredSimilarNamesAdmin)
