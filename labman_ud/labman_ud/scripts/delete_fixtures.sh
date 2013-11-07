#!/bin/bash

declare -a apps=( 'events' 'funding_programs' 'organizations' 'persons' 'projects' 'publications' 'news' 'utils' )

for app in ${apps[*]}; do
    rm entities/$app/fixtures/initial_data.json
done
