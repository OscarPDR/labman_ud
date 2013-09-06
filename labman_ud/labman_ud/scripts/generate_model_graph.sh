#!/bin/bash

python manage.py graph_models events funding_programs news organizations persons projects publications utils publications utils -g -o labman_ud_models.png --settings=labman_ud.settings.dev
