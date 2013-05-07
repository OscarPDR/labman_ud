#!/bin/bash

python manage.py dumpdata persons --indent=4 > persons/fixtures/initial_data.json
python manage.py dumpdata funding_programs --indent=4 > funding_programs/fixtures/initial_data.json
python manage.py dumpdata organizations --indent=4 > organizations/fixtures/initial_data.json
python manage.py dumpdata projects --indent=4 > projects/fixtures/initial_data.json
python manage.py dumpdata events --indent=4 > events/fixtures/initial_data.json
