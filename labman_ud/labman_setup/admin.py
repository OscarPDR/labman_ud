
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


###########################################################################
# Class: SEOAndAnalyticsAdmin
###########################################################################

class SEOAndAnalyticsAdmin(admin.ModelAdmin):
    model = SEOAndAnalytics


###########################################################################
# Class: TweetPonyConfigurationAdmin
###########################################################################

class TweetPonyConfigurationAdmin(admin.ModelAdmin):
    model = TweetPonyConfiguration


###########################################################################
# Class: ZoteroConfigurationAdmin
###########################################################################

class ZoteroConfigurationAdmin(admin.ModelAdmin):
    model = ZoteroConfiguration


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################

admin.site.register(LabmanDeployGeneralSettings, LabmanDeployGeneralSettingsAdmin)
admin.site.register(OfficialSocialProfile, OfficialSocialProfileAdmin)
admin.site.register(SEOAndAnalytics, SEOAndAnalyticsAdmin)
admin.site.register(TweetPonyConfiguration, TweetPonyConfigurationAdmin)
admin.site.register(ZoteroConfiguration, ZoteroConfigurationAdmin)
