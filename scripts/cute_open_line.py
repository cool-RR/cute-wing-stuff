# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `cute_open_line` script.

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


behaviors = ('stand-ground', 'before', 'after')



def cute_open_line(editor=wingapi.kArgEditor, behavior='stand-ground'):
    '''
    Open a new line, but don't move the caret down to the new line.
    
    Running this command is like pressing Enter, except your caret doesn't move
    into the new line that was created, but stays exactly where it was.
    
    The advantage of this over Wing's built-in `open-line` is that
    `cute-open-line` doesn't just insert a newline character like `open-line`
    does; it runs Wing's `new-line` command, which does various intelligent
    things like auto-indenting your code to the right level, opening your
    parentheses *just so* if you're doing function invocation, and a bunch of
    other goodies.
    
    If given `behavior='after'`, goes to the end of the current line, and opens
    a new line from there. If given `behavior='before'`, goes to the end of the
    previous line, and opens a new line from there.

    Suggested key combinations:
    
        `Alt-Return` for normal operation
        `Ctrl-Return` for `behavior='after'`
        `Shift-Return` for `behavior='before'`
        
    (The `Alt-Return` combination requires a AHK shim, at least on Windows.)
    '''
    
    assert isinstance(editor, wingapi.CAPIEditor)
    assert behavior in behaviors
    document = editor.GetDocument()
    with shared.UndoableAction(document):
        if behavior == 'stand-ground':
            with shared.SelectionRestorer(editor):
                _undoless_new_line(editor)
        else:
            _, caret_position = editor.GetAnchorAndCaret()
            line_number = document.GetLineNumberFromPosition(caret_position)
            if behavior == 'before':
                if line_number == 0:
                    return
                last_character_of_previous_line = \
                                           document.GetLineEnd(line_number - 1)
                editor.SetSelection(last_character_of_previous_line,
                                    last_character_of_previous_line)
                _undoless_new_line(editor)
            else:
                assert behavior == 'after'
                last_character_of_line = document.GetLineEnd(line_number)
                editor.SetSelection(last_character_of_line,
                                    last_character_of_line)
                _undoless_new_line(editor)


def _undoless_new_line(editor):
    assert isinstance(editor, wingapi.CAPIEditor)
    with shared.NonUndoableAction(editor):
        editor.ExecuteCommand('new-line')
