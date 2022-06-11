# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
]


import sys
import inspect

import wingapi

import shared

def reverse_selection():
    '''
    Reverse the selection, putting the caret on the opposite side.

    If the caret was at the beginning of the selection, it'll be put at the
    end, and if it was in the end, it'll be put in the beginning.

    Suggested key combination: `Insert Shift-R`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    app = wingapi.gApplication
    anchor_position, caret_position = editor.GetAnchorAndCaret()
    app.ExecuteCommand('set-visit-history-anchor')
    editor.SetSelection(caret_position, anchor_position)