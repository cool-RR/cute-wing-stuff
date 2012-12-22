# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import sys
import inspect

import wingapi

import shared

TAB_KEY = 15 if 'linux' in sys.platform else '48' if 'darwin' in sys.platform \
                                                                         else 9


def cute_query_replace(editor=wingapi.kArgEditor, app=wingapi.kArgApplication):
    assert isinstance(editor, wingapi.CAPIEditor)
    assert isinstance(app, wingapi.CAPIApplication)
    selection_start, selection_end = editor.GetSelection()
    selection = editor.GetDocument().GetCharRange(selection_start,
                                                  selection_end)
    
    if selection:
        editor.SetSelection(selection_start, selection_start)
        app.ExecuteCommand('query-replace')
        with shared.ClipboardRestorer():
            if shared.autopy_available:
                import autopy.key
                autopy.key.toggle(autopy.key.K_ALT, False)
                with shared.ClipboardRestorer():
                    app.SetClipboard(selection)
                    autopy.key.tap('v', autopy.key.MOD_CONTROL)
                #autopy.key.tap(autopy.key.K_ESCAPE)
                autopy.key.toggle(autopy.key.K_ALT, False)
                autopy.key.tap(TAB_KEY)
                autopy.key.tap('v', autopy.key.MOD_CONTROL)
                autopy.key.tap('a', autopy.key.MOD_CONTROL)
                autopy.key.tap('a', autopy.key.MOD_CONTROL)
                autopy.key.tap('a', autopy.key.MOD_CONTROL)
            
        
    else: # not selection
        app.ExecuteCommand('query-replace')