#!/bin/bash

declare -a apps=( 'events' 'funding_programs' 'news' 'organizations' 'persons' 'projects' 'publications' 'utils' )

mkdir entities_fixtures

for app in ${apps[*]}; do
    mkdir -p entities_fixtures/$app/fixtures
    cp entities/$app/fixtures/initial_data.json  entities_fixtures/$app/fixtures/initial_data.json
done

tar -cvf fixtures.tar entities_fixtures
