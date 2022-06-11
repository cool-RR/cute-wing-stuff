# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
]


import inspect

import wingapi

import shared


def comment_hr():
    '''
    Enter a horizontal line of "#" characters going until character 79.

    Example:

        #######################################################################

    Suggested key combination: `Insert H`
    '''

    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)

    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)

    with shared.UndoableAction(document):

        original_start, original_end = editor.GetSelection()
        original_end_line_number = \
                document.GetLineNumberFromPosition(original_end)
        original_document_length = document.GetLength()
        original_line_count = document.GetLineCount()

        indent_size = shared.get_indent_size_in_pos(editor, original_start)

        string_to_write = (' ' * indent_size) + ('#' * (79 - indent_size)) + \
                                                                           '\n'

        assert len(string_to_write) == 79

        start_line_number = document.GetLineNumberFromPosition(original_start)
        start_line_first_char = document.GetLineStart(start_line_number)
        document.InsertChars(start_line_first_char, string_to_write)

        editor.ExecuteCommand('home')