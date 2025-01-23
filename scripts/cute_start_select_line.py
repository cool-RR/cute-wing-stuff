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
    document_text = document.GetText()
    utf8_selection_start, utf8_selection_end = editor.GetSelection()
    selection_start_line = document.GetLineNumberFromPosition(utf8_selection_start)
    selection_end_line = document.GetLineNumberFromPosition(utf8_selection_end)

    utf8_new_selection_start = document.GetLineStart(selection_start_line)

    ###########################################################################
    #                                                                         #
    raw_utf8_new_selection_end = document.GetLineEnd(selection_end_line)
    utf8_two_characters_after = document_text[raw_utf8_new_selection_end :
                                         min(raw_utf8_new_selection_end + 2, document.GetLength())]
    if utf8_two_characters_after:
        if utf8_two_characters_after[0] == '\n':
            utf8_new_selection_end = raw_utf8_new_selection_end + 1
        elif utf8_two_characters_after[0] == '\r':
            if len(utf8_two_characters_after) == 2 and \
                                               utf8_two_characters_after[1] == '\n':
                utf8_new_selection_end = raw_utf8_new_selection_end + 2
            else:
                utf8_new_selection_end = raw_utf8_new_selection_end + 1
        else:
            utf8_new_selection_end = raw_utf8_new_selection_end
    else:
        utf8_new_selection_end = raw_utf8_new_selection_end
    #                                                                         #
    ###########################################################################

    _, utf8_caret_position = editor.GetAnchorAndCaret()
    if utf8_caret_position == utf8_selection_end:
        arguments = (utf8_new_selection_start, utf8_new_selection_end)
    else:
        assert utf8_caret_position == utf8_selection_start
        arguments = (utf8_new_selection_end, utf8_new_selection_start)

    wingapi.gApplication.ExecuteCommand('start-select-line')
    editor.SetSelection(*arguments)



cute_start_select_line.available = \
                                  lambda: wingapi.gApplication.CommandAvailable('start_select_line')

