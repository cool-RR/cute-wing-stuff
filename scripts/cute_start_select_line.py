# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import wingapi

import shared


def cute_start_select_line():
    '''
    Start selecting by visual lines instead of by character.

    What this adds over `start-select-line` is that it takes the current
    selection when this command is invoked and expands it to cover all of its
    lines as the initial selection.

    Suggested key combination: `Ctrl-F8`
    '''

    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    selection_start, selection_end = shared.get_selection_unicode(editor)
    selection_start_line = document.GetLineNumberFromPosition(selection_start)
    selection_end_line = document.GetLineNumberFromPosition(selection_end)

    new_selection_start = document.GetLineStart(selection_start_line)

    ###########################################################################
    #                                                                         #
    raw_new_selection_end = document.GetLineEnd(selection_end_line)
    two_characters_after = document.GetText()[raw_new_selection_end :
                                              min(raw_new_selection_end + 2, document.GetLength())]
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
    shared.set_selection_unicode(editor, *arguments)



cute_start_select_line.available = (
    lambda :
                     wingapi.gApplication.CommandAvailable('start_select_line')
)

