#!/bin/bash

python manage.py graph_models core events funding_programs news organizations persons projects publications utils zotero -g -o labman_ud_models.png --settings=labman_ud.settings.local
