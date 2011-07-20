# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `push_line_to_end` script.

See its documentation for more information.
'''


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


TARGET_LINE_LENGTH = 79
'''
The maximum number of characters that should be in one line.

The user-customized number is available through Wing settings, but because of
an off-by-one bug in Wing, it is hard-coded here.
'''


def push_line_to_end(editor=wingapi.kArgEditor):
    '''
    Push the current line to the end, aligning it to right border of editor.
    
    This inserts or deletes as many spaces as necessary from the beginning of
    the line to make the end of the line exactly coincide with the right border
    of the editor. (Whose width can be configured in the `TARGET_LINE_LENGTH`
    constant in this module.)
    
    This is useful for creating lines of this style:
    
        if first_long_condition(foo, foobar) and \
                                          second_long_condition(fubaz, bazbar):
                                          
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    position, _ = editor.GetSelection()
    line = document.GetLineNumberFromPosition(position)
    line_start = document.GetLineStart(line)
    line_end = document.GetLineEnd(line)
    current_line_length = line_end - line_start
    n_spaces_to_add = TARGET_LINE_LENGTH - current_line_length
    if n_spaces_to_add == 0:
        return
    elif n_spaces_to_add > 0:
        string_to_insert = (' ' * n_spaces_to_add)
        with shared.UndoableAction(document):
            document.InsertChars(line_start, string_to_insert)
    else:
        assert n_spaces_to_add < 0
        line_content = document.GetCharRange(line_start, line_end)
        n_spaces_to_delete = min(
            -n_spaces_to_add,
            shared.get_n_identical_edge_characters(
                line_content,
                character=' '
            )
        )    
        with shared.UndoableAction(document):   
            document.DeleteChars(
                line_start,
                line_start + (n_spaces_to_delete - 1)
            )
