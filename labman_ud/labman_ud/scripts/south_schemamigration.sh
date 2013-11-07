#!/bin/bash

declare -a apps=( 'events' 'funding_programs' 'organizations' 'persons' 'projects' 'publications' 'utils' 'news'  'zotero_labman')

for app in ${apps[*]}; do
    python manage.py schemamigration $app --auto --settings=labman_ud.settings.dev
done
