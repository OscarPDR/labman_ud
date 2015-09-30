# -*- coding: utf-8 -*-

from extractors.zotero.zotero_extractor import extract_publications_from_zotero, get_last_synchronized_zotero_version


###     synchronize_zotero()
####################################################################################################

def synchronize_zotero():
    extract_publications_from_zotero(get_last_synchronized_zotero_version())
