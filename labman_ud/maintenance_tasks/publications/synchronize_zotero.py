# -*- coding: utf-8 -*-


from extractors.zotero.zotero_extractor import extract_publications_from_zotero, _get_last_zotero_version


###########################################################################
# def: synchronize_zotero()
###########################################################################

def synchronize_zotero():
    print '#' * 80
    print 'Synchronizing publications with last version from Zotero...'
    print '#' * 80

    print '\tExtracting last publications'
    extract_publications_from_zotero(_get_last_zotero_version())
    print '\t\tExtraction completed'
