# -*- coding: utf-8 -*-

from django.conf import settings

import os
import time

import logging
logger = logging.getLogger(__name__)


def _remove_empty_folder(path, remove_root=True):

        if not os.path.isdir(path):
            return

        # Remove empty subfolders
        files = os.listdir(path)

        if len(files):
            for f in files:
                fullpath = os.path.join(path, f)

                if os.path.isdir(fullpath):
                    _remove_empty_folder(fullpath)

        # If folder empty, delete it
        files = os.listdir(path)

        if len(files) == 0 and remove_root:
            logger.info(u'\tRemoved: %s' % path)

            os.rmdir(path)


###     remove_empty_media_folders()
####################################################################################################

def remove_empty_media_folders():
    logger.debug(u'')
    logger.debug(u'Starting empty MEDIA folders removal...')
    start_time = time.time()

    _remove_empty_folder(getattr(settings, 'MEDIA_ROOT', None))

    logger.debug(u'Proccess finished (%f s)' % (time.time() - start_time))
    logger.debug(u'')
