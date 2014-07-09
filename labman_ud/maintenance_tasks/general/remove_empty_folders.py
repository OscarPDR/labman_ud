# -*- coding: utf-8 -*-

import os


###########################################################################
# def: remove_empty_folders()
###########################################################################

def remove_empty_folders(path, removeRoot=True):
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)

    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)

            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)

    if len(files) == 0 and removeRoot:
        print '#' * 80
        print "\tRemoving empty folder:", path
        print '#' * 80

        os.rmdir(path)
