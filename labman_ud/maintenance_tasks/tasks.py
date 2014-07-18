# -*- coding: utf-8 -*-


from __future__ import absolute_import

from django.core.management import call_command
from labman_ud.celery import app


@app.task(name='tasks.clean_tags')
def clean_tags():
    try:
        call_command('clean_tags')

    except:
        pass


@app.task(name='tasks.greet_birthday')
def greet_birthday():
    try:
        call_command('greet_birtday')

    except:
        pass


@app.task(name='tasks.people_management')
def people_management():
    try:
        call_command('people_management')

    except:
        pass


@app.task(name='tasks.project_management')
def project_management():
    try:
        call_command('project_management')

    except:
        pass


@app.task(name='tasks.remove_empty_folders')
def remove_empty_folders():
    try:
        call_command('remove_empty_folders')

    except:
        pass


@app.task(name='tasks.remove_unrelated_entities')
def remove_unrelated_entities():
    try:
        call_command('remove_unrelated_entities')

    except:
        pass


@app.task(name='tasks.republish_all_data_as_rdf')
def republish_all_data_as_rdf():
    try:
        call_command('republish_all_data_as_rdf')

    except:
        pass


@app.task(name='tasks.reset_publications')
def reset_publications():
    try:
        call_command('reset_publications')

    except:
        pass


@app.task(name='tasks.synchronize_zotero')
def synchronize_zotero():
    try:
        call_command('synchronize_zotero')

    except:
        pass
