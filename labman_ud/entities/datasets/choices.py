# -*- coding: utf-8 -*-

"""
This class contains the needed choice types to be inserted in the models or the forms of this django app

"""

MIN_YEAR_LIMIT = 1950
MAX_YEAR_LIMIT = 2080

FILE_FORMAT_CHOICES = (
    ('ext', 'External link'),
    ('csv', '*.csv'),
    ('zip', '*.zip'),
    ('xls', '*.xls'),
    ('xlsx', '*.xlsx'),
    ('xlm', '*.xlm'),
    ('json', '*.json'),
    ('geojson', '*.geojson'),
    ('jpeg', '*.jpeg'),
    ('kml', '*.kml'),
    ('shp', '*.shp'),
    ('sql', '*.sql'),
    ('R', '*.R'),
    ('jsonld', '*.jsonld'),
    ('dat', '*.dat'),
)

LICENSE_CHOICES = (
    ('ne', 'Not specified'),
    ('gpl', 'General Public License'),
    ('odc', 'Open Data Commons'),
    ('cc', 'Creative Commons'),
    ('ogl', 'Open Government License'),
    ('ncgl', 'Non-Commercial Government Licence'),
    ('pd', 'Public Domain'),
    ('mit', 'MIT License'),
    ('ap', 'Apache Public License'),
)

SELECTION_CHOICES = (
    ('<', 'Less'),
    ('<=', 'Less or Equal'),
    ('>', 'Greater'),
    ('>=', 'Greater or Equal'),
    ('==', 'Equal')
)
