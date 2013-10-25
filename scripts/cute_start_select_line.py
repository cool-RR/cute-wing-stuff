# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `cute_start_select_line` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import wingapi

import shared


def cute_start_select_line(editor=wingapi.kArgEditor):
    '''
    Start selecting by visual lines instead of by character.
    
    What this adds over `start-select-line` is that it takes the current
    selection when this command is invoked and expands it to cover all of its
    lines as the initial selection.

    Suggested key combination: `Ctrl-F8`
    '''
    
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    selection_start, selection_end = editor.GetSelection()
    selection_start_line = document.GetLineNumberFromPosition(selection_start)
    selection_end_line = document.GetLineNumberFromPosition(selection_end)
    
    new_selection_start = document.GetLineStart(selection_start_line)
    
    ###########################################################################
    #                                                                         #
    raw_new_selection_end = document.GetLineEnd(selection_end_line)
    two_characters_after = document.GetCharRange(
        raw_new_selection_end,
        min(
            raw_new_selection_end + 2,
            document.GetLength()
        )
    )
    if two_characters_after:
        if two_characters_after[0] == '\n':
            new_selection_end = raw_new_selection_end + 1
        elif two_characters_after[0] == '\r':
            if len(two_characters_after) == 2 and \
                                               two_characters_after[1] == '\n':
                new_selection_end = raw_new_selection_end + 2
            else:
                new_selection_end = raw_new_selection_end + 1
        else:
            new_selection_end = raw_new_selection_end
    else:
        new_selection_end = raw_new_selection_end
    #                                                                         #
    ###########################################################################
    
    _, caret_position = editor.GetAnchorAndCaret()
    if caret_position == selection_end:
        arguments = (new_selection_start, new_selection_end)
    else:
        assert caret_position == selection_start
        arguments = (new_selection_end, new_selection_start)
        
    wingapi.gApplication.ExecuteCommand('start-select-line')
    editor.SetSelection(*arguments)
    


cute_start_select_line.available = (
    lambda editor=wingapi.kArgEditor:
                     wingapi.gApplication.CommandAvailable('start_select_line')
)

