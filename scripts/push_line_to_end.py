# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]

from python_toolbox import string_tools

import wingapi

import shared


def _get_n_identical_edge_characters(string, character=None, head=True):
    '''
    Get the number of identical characters at `string`'s head.

    For example, the result for 'qqqwe' would be `3`, while the result for
    'meow' will be `1`.

    Specify `character` to only consider that character; if a different
    character is found at the head, `0` will be returned.

    Specify `head=False` to search the tail instead of the head.
    '''
    if not string:
        return 0
    index = 0 if head is True else -1
    direction = 1 if head is True else -1
    if character is None:
        character = string[index]
    else:
        assert isinstance(character, basestring) and len(character) == 1
    for i, c in enumerate(string[::direction]):
        if c != character:
            return i
    else:
        return len(string)


def push_line_to_end(line_offset=0):
    '''
    Push the current line to the end, aligning it to right border of editor.

    This inserts or deletes as many spaces as necessary from the beginning of
    the line to make the end of the line exactly coincide with the right border
    of the editor. (Whose width can be configured in Wing's "Preferences" ->
    "Line Wrapping" -> "Reformatting Wrap Column".)

    This is useful for creating lines of this style:

        if first_long_condition(foo, foobar) and \
                                          second_long_condition(fubaz, bazbar):

    Also deletes trailing spaces.

    Suggested key combination: `Insert End`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    position, _ = shared.get_selection_unicode(editor)
    line = document.GetLineNumberFromPosition(position) + line_offset
    line_start = document.GetLineStart(line)
    line_end = document.GetLineEnd(line)
    line_content = document.GetCharRange(line_start, line_end)
    n_trailing_spaces = _get_n_identical_edge_characters(line_content,
                                                         character=' ',
                                                         head=False)
    current_line_length = line_end - line_start
    n_spaces_to_add = \
        wingapi.gApplication.GetPreference('edit.text-wrap-column') - \
                                        current_line_length + n_trailing_spaces

    with shared.UndoableAction(document):
        document.DeleteChars(line_end - n_trailing_spaces, line_end - 1)
        if n_spaces_to_add == 0:
            return
        elif n_spaces_to_add > 0:
            string_to_insert = (' ' * n_spaces_to_add)
            document.InsertChars(line_start, string_to_insert)
        else:
            assert n_spaces_to_add < 0
            n_spaces_to_delete = min(
                -n_spaces_to_add,
                string_tools.get_n_identical_edge_characters(
                    line_content,
                    character=' '
                )
            )
            document.DeleteChars(
                line_start,
                line_start + (n_spaces_to_delete - 1)
            )

