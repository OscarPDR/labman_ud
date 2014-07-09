# -*- coding: utf-8 -*-


from entities.projects.models import Project


###########################################################################
# def: check_non_filled_dates()
###########################################################################

def check_non_filled_dates():
    print '#' * 80
    print 'Checking for incomplete project dates info...'
    print '#' * 80

    projects_without_start_month = Project.objects.filter(start_month='')

    for project in projects_without_start_month:
        print '\t\t%s has no start_month' % project.short_name

        project.start_month = 1
        project.save()

        print '\t\t%s\'s start_month set to 1 by default' % project.short_name

    projects_without_end_month = Project.objects.filter(end_month='')

    for project in projects_without_end_month:
        print '\t\t%s has no end_month' % project.short_name

        project.end_month = 12
        project.save()

        print '\t\t%s\'s end_month set to 12 by default' % project.short_name
