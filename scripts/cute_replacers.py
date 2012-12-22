# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import time
import threading
import inspect

import wingapi

import shared


def cute_query_replace(editor=wingapi.kArgEditor, app=wingapi.kArgApplication):
    assert isinstance(editor, wingapi.CAPIEditor)
    selection_start, selection_end = editor.GetSelection()
    selection = editor.GetDocument().GetCharRange(selection_start,
                                                  selection_end)
    
    if selection:
        editor.SetSelection(selection_start, selection_start)
        app.ExecuteCommand('query-replace')
        if shared.autopy_available:
            import autopy.key
            autopy.key.toggle(autopy.key.K_ALT, False)
            autopy.key.type_string(selection)
            #def _do():
                #time.sleep(0.05)
            autopy.key.tap(9)
            autopy.key.tap('v', autopy.key.MOD_CONTROL)
            #thread = threading.Thread(target=_do)
            #thread.start()
            
        
    else: # not selection
        app.ExecuteCommand('query-replace')