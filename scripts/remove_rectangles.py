# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import wingapi

import shared


def remove_rectangles(editor=wingapi.kArgEditor):
    '''
    Remove all rectangles that Wing drew on the editor.
    
    Wing sometimes draws rectangles on the editor, either for search results or
    for highlighting appearances of the currently selected word. This command
    clears all of those squares.
    
    Suggested key combination: `Insert Ctrl-R`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    editor.fEditor.fEditMgr.fOccurrences._ClearAll(
        [editor.fEditor.fCache.fDoc]
    )
    