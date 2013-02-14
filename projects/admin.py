from django.contrib import admin
from projects.models import Project, FundingAmount, AssignedEmployee, ConsortiumMember

admin.site.register(Project)
admin.site.register(FundingAmount)
admin.site.register(AssignedEmployee)
admin.site.register(ConsortiumMember)
