#!/bin/bash

declare -a apps=( 'events' 'funding_programs' 'organizations' 'persons' 'projects' 'publications' 'utils' 'news' 'zotero_labman')

for app in ${apps[*]}; do
    python manage.py migrate $app --delete-ghost-migrations --settings=labman_ud.settings.local
done
