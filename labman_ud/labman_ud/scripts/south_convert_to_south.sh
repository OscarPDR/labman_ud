#!/bin/bash

declare -a apps=( 'events' 'funding_programs' 'organizations' 'persons' 'projects' 'publications' 'utils' 'zotero_labman')

for app in ${apps[*]}; do
    python manage.py convert_to_south $app
done
