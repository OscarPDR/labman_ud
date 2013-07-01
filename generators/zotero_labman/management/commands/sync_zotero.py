#encoding: utf-8 

from pyzotero import zotero
from dateutil import parser
import requests
import json
import os

from django.core.management.base import NoArgsCommand

from labman_ud import settings

class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Synchronizes your Zotero library with Labman.'

    def handle_noargs(self, **options):
        self.__api_key = getattr(settings, 'ZOTERO_API_KEY', None)
        self.__library_id = getattr(settings, 'ZOTERO_LIBRARY_ID', None)
        self.__library_type = getattr(settings, 'ZOTERO_LIBRARY_TYPE', None)
        self.__pdf_path = getattr(settings, 'MEDIA_ROOT', None)
        self.__api_limit = 5
        
        # TODO: Check variables

        self.__parse_last_items()

    def __parse_last_items(self):
        zot = zotero.Zotero(self.__library_id, self.__library_type, self.__api_key)

        # Get last updated item from the json file
        lastkey, lastdt = self.__get_last_updated()

        gen = zot.makeiter(zot.top(limit=self.__api_limit, order='dateModified', sort='desc'))

        new_lastkey = ''
        new_lastdt = None
        lastitems = []

        moreitems = True
        while moreitems:
            try:
                items = gen.next()
            except StopIteration:
                moreitems = False

            if items != lastitems:
                for item in items:
                    if item['itemType'] in ['bookSection', 'book', 'journalArticle', 'magazineArticle', 'newspaperArticle', 'thesis', 'report', 'patent', 'presentation', 'conferencePaper', 'document']:
                        if lastdt is not None and parser.parse(item['updated']) <= lastdt:
                            moreitems = False
                            break
                        else:
                            if new_lastdt is None:
                                new_lastkey = item['key']
                                new_lastdt = item['updated']

                            print item
                            #print item['itemType']
                            print item['title'].encode('utf-8')

                            # A second connection to Zotero API is needed for the retrieval of children, otherwise the iterator stops
                            zot_children = zotero.Zotero(self.__library_id, self.__library_type, self.__api_key)
                            children = zot_children.children(item['key'])
                            
                            for child in children:
                                if child['itemType'] == 'attachment' and child['contentType'] == 'application/pdf':
                                    print "Getting " + child['filename'] + '...'
                                    r = requests.get('https://api.zotero.org/'+  self.__library_type + 's/'+ self.__library_id + '/items/'+ child['key'] + '/file?key=' + self.__api_key)
                                    with open(self.__pdf_path + '/' + item['key'] + '_' + child['filename'], "wb") as pdffile:
                                        pdffile.write(r.content)
                            print '-'*30
                lastitems = items

        if new_lastdt is not None:
            with open(self.__pdf_path + '/' + '.lastupdate.json', 'w') as jsonfile:
                json.dump({'key': new_lastkey, 'date': new_lastdt}, jsonfile)

    def __get_last_updated(self):
        try:
            with open(self.__pdf_path + '/' + '.lastupdate.json', 'r') as jsonfile:
                lastupdate = json.load(jsonfile)
                return lastupdate['key'], parser.parse(lastupdate['date'])
        except IOError:
            return None, None