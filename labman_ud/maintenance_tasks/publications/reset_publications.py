# -*- coding: utf-8 -*-

from extractors.zotero.zotero_extractor import extract_publications_from_zotero


###     reset_publications()
####################################################################################################

def reset_publications():
    extract_publications_from_zotero(0)
