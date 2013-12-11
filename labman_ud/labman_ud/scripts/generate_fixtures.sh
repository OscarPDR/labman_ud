#!/bin/bash

declare -a apps=( 'events' 'funding_programs' 'news' 'organizations' 'persons' 'projects' 'publications' 'utils' )

today=$(date +"%m_%d_%Y")

for app in ${apps[*]}; do
    mkdir -p entities/$app/fixtures
    if [ -f entities/$app/fixtures/initial_data.json ]; then
        mv entities/$app/fixtures/initial_data.json entities/$app/fixtures/initial_data_$today.json
    fi
    python manage.py dumpdata $app --indent=4 > entities/$app/fixtures/initial_data.json --settings=labman_ud.settings.dev
done
