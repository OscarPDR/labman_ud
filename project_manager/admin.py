from django.contrib import admin
from project_manager.models import Project, FundingProgram, FundingAmount, AssignedEmployee, ConsortiumMember

admin.site.register(Project)
admin.site.register(FundingProgram)
admin.site.register(FundingAmount)
admin.site.register(AssignedEmployee)
admin.site.register(ConsortiumMember)
