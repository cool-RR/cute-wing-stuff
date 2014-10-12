# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import string as string_module
import sys
import os
import inspect

import wingapi
import guiutils.widgets_qt4
import wingide
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
        from guiutils.widgets_qt4 import os, sys, textutils, location, fileutils
        # Utility to obtain list of files for directory on disk
        dirname, filefrag = os.path.split(textutils.AsUnicode(entry))
        try:
            file_list = location.ListDir(os.path.expanduser(dirname), log_error=False)
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

    
    old_ExpandFileFragment = guiutils.widgets_qt4.ExpandFileFragment
    guiutils.widgets_qt4.ExpandFileFragment = ExpandFileFragment
    
    ###########################################################################
    
    def _get_location_path(location):
        import wingutils.location
        if sys.platform == 'win32':
            return location._fOSName
        else:
            return location._fOSName.encode(
                wingutils.location.kFileSystemEncoding
            )
        
 
    def _open(self, filenames):
        from wingide.topcommands import location, logging, prefs
        # Get file location object
        loc_list = [location.CreateFromName(name) for name in filenames]
    
        for loc in loc_list:
            if loc.IsDirectory():
                path = _get_location_path(loc)
                shared.open_path_in_explorer(path)
            else:
                opened = False
    
                # If so configured, open any project as a project if possible; if fail
                # to do so, then open it as text
                if not self.fGuiMgr.fPrefMgr.GetValue(prefs.kOpenProjectsAsText):
                    parts = loc.fUrl.split('.')
                    if parts[-1] == 'wpr' or parts[-1] == 'wpu':
                        self.fSingletons.fWingIDEApp.fProjMgr.OpenProject(loc)
                        opened = True
    
                if not opened:
                    # Open the file into active document window
                    win = self.fGuiMgr.GetActiveDocumentWindow()
                    src_text = self.fGuiMgr.DisplayDocument(loc, blank_if_not_found=True,
                                                            win=win, sticky=True)
                    
    wingide.topcommands.CApplicationControlCommands._open = _open
    
    ###########################################################################
    
    def set_perspective_nicely(*args, **kwargs):
        wingapi.gApplication.ExecuteCommand('perspective-restore',
                                            name='Turing')
        if shared.autopy_available:
            autopy.key.tap('q', autopy.key.MOD_ALT | autopy.key.MOD_META)
        
    # wingapi.gApplication.connect('project-open', set_perspective_nicely)
    
    ###########################################################################
    

    if shared.autopy_available:
        import autopy.key
        
        def analyze_text_modified(*args):
            flag, text = args[3:5]
            if flag == 2 and text[-1] in string_module.whitespace:
                shared.clip_ahk()
                
        cache.textcache.CTextCache.class_connect('text-modified',
                                                 analyze_text_modified)
    

        #######################################################################
        
        import singleton
        
        commands_to_clip_after = set(
            ['introduce_variable', 'rename_symbol', 'extract_def',
             'arg_to_attr', 'deep_to_var']
        )
            
        def command_executed(command_manager, command, args):
            if command.name in commands_to_clip_after:
                shared.clip_ahk()
        
        wingapi.gApplication.fSingletons.fCmdMgr.connect('cmd-executed',
                                                         command_executed)
        
        #######################################################################
        
        def args_needed(*args, **kwargs):
            shared.clip_ahk()
            
        wingapi.gApplication.fSingletons.fCmdMgr.connect('args-needed',
                                                         args_needed)
        
        
        