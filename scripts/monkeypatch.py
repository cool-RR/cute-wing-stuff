# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import string as string_module
import sys
import inspect

import wingapi
import guiutils.widgets_gtk
import cache.textcache

import shared


_ignore_scripts = True

# Must set `monkeypatch = True` in `cute_wing_stuff_local_settings.py` for this
# module to work!

try:
    import cute_wing_stuff_local_settings
except ImportError:
    monkeypatch = False
else:
    monkeypatch = cute_wing_stuff_local_settings.monkeypatch
    
    
if monkeypatch:

    # Monkeypatching `ExpandFileFragment` so Wing won't show .pyc, .pyo and
    # .pyd files when browsing using `open-from-keyboard`:
    
    def ExpandFileFragment(entry):
        """ Try to expand given entry for possible matches, completing as far
        as we can """
        from guiutils.widgets_gtk import *
        # Utility to obtain list of files for directory on disk
        dirname, filefrag = os.path.split(textutils.AsUnicode(entry))
        if not dirname:
            return []
        try:
            file_list = location.ListDir(os.path.expanduser(dirname))
        except OSError:
            file_list = []
    
        allfiles = []
        for file in file_list:
            # This is the only modified part.
            ### Throwing away compiled Python files: ##########################
            #                                                                 #
            if file.endswith('.pyc') or file.endswith('.pyo') or \
                                                         file.endswith('.pyd'):
                continue
            #                                                                 #
            ### Finished throwing away compiled Python files. #################
            if sys.platform == 'win32':
                file_matches = file.lower().startswith(filefrag.lower())
            else:
                file_matches = file.startswith(filefrag)
            if file_matches:
                match = fileutils.join(dirname, file)
                if os.path.isdir(match) and match[-1] != os.sep:
                    match = match + os.sep
                allfiles.append(match)
    
        return allfiles
    
    
    old_ExpandFileFragment = guiutils.widgets_gtk.ExpandFileFragment
    guiutils.widgets_gtk.ExpandFileFragment = ExpandFileFragment
    
    ###########################################################################

    if shared.autopy_available:
        import autopy.key
        
        def analyze_text_modified(*args):
            flag, text = args[3:5]
            print('first')
            #autopy.key.tap('x')
            if flag == 2 and text[-1] in string_module.whitespace:
                print('second')
                autopy.key.tap(135)
                #autopy.key.tap('x')
                
        cache.textcache.CTextCache.class_connect('text-modified',
                                                 analyze_text_modified)
    
