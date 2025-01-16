# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import re

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]

import wingapi
from pysource import strutils

import shared

range_pattern = re.compile('^(x?range)\(.*\)$')


def for_thing_in_things(comprehension=False):
    '''
    Turn `things` into `for thing in things:`.

    Type any pluarl word, like `bananas` or `directories`. Then run this
    script, and you get `for directory in directories`.

    This also works for making `range(number)` into `for i in range(number):`.

    Note: The `:` part is added only on Windows.

    If `comprehension=True`, inputs `for thing in things` without the colon and
    puts the caret before instead of after.

    Suggested key combination: `Insert Ctrl-F`
                               `Insert Shift-F` for `comprehension=True`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    document_text = shared.get_text(document)

    assert isinstance(document, wingapi.CAPIDocument)

    with shared.UndoableAction(document):
        end_position_utf8, _ = editor.GetSelection()
        end_position = strutils.CharOffsetForUtf8Offset(document_text, end_position_utf8)
        line_number_utf8 = document.GetLineNumberFromPosition(end_position_utf8)
        line_start_utf8 = document.GetLineStart(line_number_utf8)
        line_start = strutils.CharOffsetForUtf8Offset(document_text, line_start_utf8)
        line_end_utf8 = document.GetLineEnd(line_number_utf8)
        line_end = strutils.CharOffsetForUtf8Offset(document_text, line_end_utf8)
        line_contents = document_text[line_start : line_end]
        shared.set_selection_unicode(editor, end_position, end_position)
        if ')' in document_text[end_position - 1 : end_position + 1] \
                                                 and 'range(' in line_contents:

            text_start_position = document_text.find('range(', line_start)
            if document_text[text_start_position - 1] == 'x':
                text_start_position -= 1
            end_position = document_text.find(
                ')',
                text_start_position,
                min((line_end, end_position + 1))
            ) + 1
        else:
            wingapi.gApplication.ExecuteCommand('backward-word')
            text_start_position, _ = shared.get_selection_unicode(editor)
            wingapi.gApplication.ExecuteCommand('forward-word')
            wingapi.gApplication.ExecuteCommand('select-expression')
            shared.strip_selection_if_single_line(editor)
            expression_start_position_utf8, _ = editor.GetSelection()


        base_text = document_text[text_start_position : end_position]
        ### Analyzing base text: ##############################################
        #                                                                     #
        if range_pattern.match(base_text):
            variable_name = 'i'
        elif base_text.endswith('s'):
            variable_name = shared.plural_word_to_singular_word(base_text)
        else:
            raise Exception('This text doesn\'t work: %s' % base_text)
        #                                                                     #
        ### Finished analyzing base text. #####################################

        segment_to_insert = 'for %s in ' % variable_name

        with shared.SelectionRestorer(editor):
            app.ExecuteCommand('beginning-of-line-text(toggle=False)')
            home_position_utf8, _ = editor.GetSelection()
            home_position = strutils.CharOffsetForUtf8Offset(document_text, home_position_utf8)

        if comprehension:
            segment_to_insert = ' %s' % segment_to_insert
            document.InsertChars(expression_start_position_utf8, segment_to_insert)
            editor.SetSelection(expression_start_position_utf8,
                                expression_start_position_utf8)
        else:
            document.InsertChars(home_position_utf8, segment_to_insert)
            wingapi.gApplication.ExecuteCommand('colon-at-end')
