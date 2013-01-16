from django.contrib import admin
from project_manager.models import Project, FundingProgram, FundingAmount


admin.site.register(Project)
admin.site.register(FundingProgram)
admin.site.register(FundingAmount)
