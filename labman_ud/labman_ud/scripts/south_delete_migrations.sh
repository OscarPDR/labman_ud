#!/bin/bash

declare -a apps=( 'events' 'funding_programs' 'organizations' 'persons' 'projects' 'publications' 'utils' )
declare -a generators=( 'zotero_labman' )

for app in ${apps[*]}; do
    rm -rf entities/$app/migrations/
done

for gen in ${generators[*]}; do
    rm -rf generators/$gen/migrations/
done
