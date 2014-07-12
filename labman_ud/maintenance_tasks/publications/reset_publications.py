# -*- coding: utf-8 -*-


from extractors.zotero.zotero_extractor import clean_database, extract_publications_from_zotero


###########################################################################
# def: reset_publications()
###########################################################################

def reset_publications():
    print '#' * 80
    print 'Extracting all publications from zotero from scratch...'
    print '#' * 80

    print '\tCleaning database...'
    clean_database()
    print '\t\tDatabase cleaned'

    print '\tExtracting all publications'
    extract_publications_from_zotero(0)
    print '\t\tExtraction completed'
