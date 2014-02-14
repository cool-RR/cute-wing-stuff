# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import guimgr.multieditor
import wingapi

import shared


def cute_goto_definition(editor=wingapi.kArgEditor):
    '''
    Go to the definition of the symbol that the caret is on.
    
    This is an improvement over Wing's `goto-selected-symbol-defn` because if
    operated when selecting a segment of code, it looks at the end of the
    selection instead of the start.
    
    Suggested key combination: `F4`
    '''

    assert isinstance(editor, wingapi.CAPIEditor)
    wingapi.gApplication.ExecuteCommand('set-visit-history-anchor')    
    selection_start, selection_end = editor.GetSelection()
    editor.SetSelection(selection_end, selection_end)
    if wingapi.gApplication.CommandAvailable('goto-selected-symbol-defn'):
        wingapi.gApplication.ExecuteCommand('goto-selected-symbol-defn')
    else:
        editor.SetSelection(selection_start, selection_end)
    wingapi.gApplication.ExecuteCommand('set-visit-history-anchor')    