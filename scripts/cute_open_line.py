# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
]

import wingapi

import shared



def cute_open_line(line_offset=0, stand_ground=False):
    '''
    Open a new line. (i.e. enter a newline character.)

    If `line_offset` is set to `-1`, it will open a line at the line above. If
    `line_offset` is set to `1`, it will open a line at the line below.

    If `stand_ground=True`, it will make the caret not move when doing the
    newline.

    (The advantage of this over Wing's built-in `open-line` is that
    `cute-open-line` doesn't just insert a newline character like `open-line`
    does; it runs Wing's `new-line` command, which does various intelligent
    things like auto-indenting your code to the right level, opening your
    parentheses *just so* if you're doing function invocation, and a bunch of
    other goodies.)

    Suggested key combinations:

        `Alt-Return` for `stand_ground=True`
        `Shift-Return` for `line_offset=-1`
        `Ctrl-Return` for `line_offset=1`
        `Alt-Shift-Return` for `line_offset=-1, stand_ground=True`
        `Ctrl-Alt-Return` for `line_offset=1, stand_ground=True`

    (The `Alt-Return` combination requires a AHK shim, at least on Windows.)
    '''

    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    assert line_offset in (-1, 0, 1)
    document = editor.GetDocument()

    context_managers = [shared.UndoableAction(document)]
    if stand_ground:
        context_managers.append(
            shared.SelectionRestorer(
                editor, line_wise=True,
                line_offset=(1 if line_offset==-1 else 0)
            )
        )

    with shared.nested(*context_managers):
        if line_offset == 0:
            editor.ExecuteCommand('new-line')
        else:
            _, caret_position = editor.GetAnchorAndCaret()
            line_number = document.GetLineNumberFromPosition(caret_position)
            if line_offset == -1:
                if line_number == 0:
                    return
                last_character_of_previous_line = \
                                           document.GetLineEnd(line_number - 1)
                editor.SetSelection(last_character_of_previous_line,
                                    last_character_of_previous_line)
                editor.ExecuteCommand('new-line')
            else:
                assert line_offset == 1
                last_character_of_line = document.GetLineEnd(line_number)
                editor.SetSelection(last_character_of_line,
                                    last_character_of_line)
                editor.ExecuteCommand('new-line')


