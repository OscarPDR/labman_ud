
from django.contrib import admin

from .models import *


# Register your models here.


###########################################################################
# Class: LabmanDeployGeneralSettingsAdmin
###########################################################################

class LabmanDeployGeneralSettingsAdmin(admin.ModelAdmin):
    model = LabmanDeployGeneralSettings


###########################################################################
# Class: OfficialSocialProfileAdmin
###########################################################################

class OfficialSocialProfileAdmin(admin.ModelAdmin):
    model = OfficialSocialProfile

    list_display = ['name', 'profile_link']
    exclude = ['slug']


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################

admin.site.register(LabmanDeployGeneralSettings, LabmanDeployGeneralSettingsAdmin)
admin.site.register(OfficialSocialProfile, OfficialSocialProfileAdmin)
