#!/bin/bash

declare -a apps=( 'utils' 'organizations' 'persons' 'news' 'projects' 'funding_programs' 'news' 'publications')

for app in ${apps[*]}; do
    python manage.py loaddata entities/$app/fixtures/initial_data.json --settings=labman_ud.settings.dev
done
