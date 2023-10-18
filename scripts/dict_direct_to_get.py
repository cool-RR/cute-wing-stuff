# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import re
import inspect

import wingapi

import shared


pattern = re.compile(
    r'''.*?(?P<square_brackets>\[(?P<key>.*?)\])$'''
)

def dict_direct_to_get():
    '''
    Turn `foo[bar]` into `foo.get(bar, None)`.

    Suggested key combination: `Insert Ctrl-G`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)

    _, current_position = editor.GetSelection()
    current_line_number = document.GetLineNumberFromPosition(current_position)

    line_start = document.GetLineStart(current_line_number)
    line_end = document.GetLineEnd(current_line_number)

    fixed_position = max(current_position - 1, line_start)

    line_head = document.GetCharRange(line_start, fixed_position)
    line_tail = document.GetCharRange(fixed_position, line_end)
    line_text = line_head + line_tail

    if ']' not in line_tail:
        #print('''']' not in line_tail''')
        return

    first_closing_bracket_position = line_tail.find(']') + len(line_head) + \
                                                                     line_start

    text_until_closing_bracket = document.GetCharRange(
        line_start,
        first_closing_bracket_position + 1
    )

    match = pattern.match(text_until_closing_bracket)
    if not match:
        #print('''no match''')
        #print('{{{%s}}}' % text_until_closing_bracket)
        return
    else: # we have a match
        square_brackets_position = \
            line_text.find(match.group('square_brackets'))
        text_to_insert = '.get(%s, None)' % match.group('key')
        new_line_text = line_text.replace(
            match.group('square_brackets'), text_to_insert
        )
        none_start = line_start + square_brackets_position + \
                                                        len(text_to_insert) - 5
        none_end = line_start + square_brackets_position + \
                                                        len(text_to_insert) - 1

        with shared.UndoableAction(document):
            document.DeleteChars(line_start, line_end - 1)
            # The `- 1` above is necessary for \n-documents.
            document.InsertChars(line_start, new_line_text)
            editor.SetSelection(none_start, none_end)


