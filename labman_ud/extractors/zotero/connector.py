
from django.db.models import Max
from extractors.zotero.models import ZoteroExtractorLog
from labman_setup.models import ZoteroConfiguration
from pyzotero import zotero

import requests


####################################################################################################
# def: get_zotero_variables()
####################################################################################################

def get_zotero_variables():
    try:
        zotero_config = ZoteroConfiguration.objects.get()

        base_url = zotero_config.base_url
        api_key = zotero_config.api_key
        library_id = zotero_config.library_id
        library_type = zotero_config.library_type

        return base_url, api_key, library_id, library_type

    except:
        print "ZoteroConfiguration object not configured in admin panel"

        return '', '', '', ''


####################################################################################################
# def: get_zotero_connection()
####################################################################################################

def get_zotero_connection():
    base_url, api_key, library_id, library_type = get_zotero_variables()

    pyzotero_connection = zotero.Zotero(library_id=library_id, library_type=library_type, api_key=api_key)

    return pyzotero_connection


####################################################################################################
# def: get_last_zotero_library_version()
####################################################################################################

def get_last_zotero_library_version():
    pyzotero_connection = get_zotero_connection()

    items = pyzotero_connection.items(limit=1)

    if len(items):
        latest_version_number = items[0]['version']

    else:
        latest_version_number = 0

    return latest_version_number


####################################################################################################
# def: get_last_locally_synchronized_zotero_version()
####################################################################################################

def get_last_locally_synchronized_zotero_version():
    try:
        last_version = ZoteroExtractorLog.objects.all().aggregate(Max('version'))['version__max']

        if last_version is None:
            last_version = 0

    except:
        last_version = 0

    return last_version


####################################################################################################
# def: update_tag_for_item()
####################################################################################################

def update_tag_for_item(pyzotero_connector, item, old_tag, new_tag):
    legacy_tags = item['data']['tags']

    for legacy_tag in legacy_tags:
        if legacy_tag['tag'] == old_tag:
            legacy_tag['tag'] = new_tag

    pyzotero_connector.update_item(item)


####################################################################################################
# def: item_has_tag()
####################################################################################################

def item_has_tag(pyzotero_connector, item, tag):
    for existing_tag in item['data']['tags']:
        if existing_tag['tag'] == tag:
            return True

    return False


####################################################################################################
# def: get_item_keys_using_tag()
####################################################################################################

def get_item_keys_using_tag(pyzotero_connector, tag):
    item_keys = set()

    if get_number_of_items_using_tag(tag) > 0:
        for item in pyzotero_connector.items():
            if item_has_tag(pyzotero_connector, item, tag):
                item_keys.add(item['data']['key'])

    return item_keys


####################################################################################################
# def: remove_tag_from_library()
####################################################################################################

def remove_tag_from_library(tag_to_remove):
    base_url, api_key, library_id, library_type = get_zotero_variables()

    url = '%s/%ss/%d/tags' % (base_url, library_type, library_id)

    headers = {
        'Zotero-API-Version': 3,
        'If-Unmodified-Since-Version': 1000000000,
        'If-Modified-Since-Version': 0,
    }

    params = {
        'key': api_key,
        'tag': tag_to_remove,
    }

    requests.delete(url, headers=headers, params=params)


####################################################################################################
# def: get_number_of_items_using_tag()
####################################################################################################

def get_number_of_items_using_tag(tag):
    base_url, api_key, library_id, library_type = get_zotero_variables()

    url = '%s/%ss/%d/tags' % (base_url, library_type, library_id)

    headers = {
        'Zotero-API-Version': 3,
    }

    params = {
        'key': api_key,
        'tag': tag,
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        return r.json()[0]['meta']['numItems']

    except:
        return 0


####################################################################################################
# def: get_number_of_items_using_tag()
####################################################################################################

def update_tag(pyzotero_connector, item, old_tag, new_tag):
    usage_keys = get_item_keys_using_tag(pyzotero_connector, old_tag)

    for item_key in usage_keys:
        update_tag_for_item(pyzotero_connector, pyzotero_connector.item(item_key), old_tag, new_tag)
