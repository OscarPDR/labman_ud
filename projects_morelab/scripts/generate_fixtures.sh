#!/bin/bash

python manage.py dumpdata persons --indent=4 > entities/persons/fixtures/initial_data.json
python manage.py dumpdata funding_programs --indent=4 > entities/funding_programs/fixtures/initial_data.json
python manage.py dumpdata organizations --indent=4 > entities/organizations/fixtures/initial_data.json
python manage.py dumpdata projects --indent=4 > entities/projects/fixtures/initial_data.json
python manage.py dumpdata events --indent=4 > entities/events/fixtures/initial_data.json
python manage.py dumpdata publications --indent=4 > entities/publications/fixtures/initial_data.json
