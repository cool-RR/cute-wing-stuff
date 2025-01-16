# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines string-selecting scripts.

See its documentation for more information.
'''

from __future__ import with_statement

import re
import _ast
import string

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import wingapi
import edit

import shared

def _is_position_on_string(editor: wingapi.CAPIEditor, position, try_previous=True):
    '''Is there a string in the specified position in the document?'''
    return (
        shared.get_char_type_unicode(editor, position) == edit.editor.kStringCharType or
        (try_previous and position >= 1 and
         (shared.get_char_type_unicode(editor, position - 1) ==
                                                  edit.editor.kStringCharType))
    )


def _find_string_from_position(editor, position, multiline=False):
    '''
    Given a character in the document known to be in a string, find its string.
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    assert _is_position_on_string(editor, position)
    document = editor.GetDocument()
    document_text = document.GetText()
    document_start = 0
    document_end = len(document_text)
    start_marker = end_marker = position
    while end_marker < document_end and \
                            _is_position_on_string(editor, end_marker+1):
        end_marker += 1
    while start_marker > document_start and \
                          _is_position_on_string(editor, start_marker-1):
        start_marker -= 1

    if start_marker > document_start:
        assert not _is_position_on_string(editor, start_marker-1)
    if end_marker < document_end:
        assert not _is_position_on_string(editor, end_marker+1)

    if multiline:
        string_ranges = [(start_marker, end_marker)]

        ### Scanning backward: ################################################
        #                                                                     #
        while True:
            start_of_first_string = string_ranges[0][0]
            # No backwards regex search in `re` yet, doing it manually:
            for i in range(start_of_first_string - 1, 0, -1):
                if document_text[i] not in string.whitespace:
                    candidate_end_of_additional_string = i
                    print('Candidate: %s %s' % (i, document_text[i]))
                    break
            else:
                break

            if _is_position_on_string(editor,
                       candidate_end_of_additional_string, try_previous=False):
                string_ranges.insert(
                    0,
                    _find_string_from_position(
                        editor,
                        candidate_end_of_additional_string
                    )
                )
                continue
            else:
                break
        #                                                                     #
        ### Finished scanning backward. #######################################

        ### Scanning forward: #################################################
        #                                                                     #
        while True:
            end_of_last_string = string_ranges[-1][1]
            search_result = re.search('\S',
                                      document_text[end_of_last_string:])
            if search_result:
                candidate_start_of_additional_string = \
                                   end_of_last_string + search_result.span()[0]
                if _is_position_on_string(editor,
                                          candidate_start_of_additional_string,
                                          try_previous=False):
                    string_ranges.append(
                        _find_string_from_position(
                            editor,
                            candidate_start_of_additional_string
                        )
                    )
                    continue

            # (This is like an `else` clause for both the above `if`s.)
            return tuple(string_ranges)
        #                                                                     #
        ### Finished scanning forward. ########################################


    else: # not multiline
        return (start_marker, end_marker)

def select_next_string(inner=False):
    '''
    Select the next (or current) string, starting from caret location.

    Provide `inner=True` to select only the contents of the string.

    Suggested key combinations: `Ctrl-Apostrophe`
                                `Alt-Apostrophe` for `inner=True`

    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    app.ExecuteCommand('set-visit-history-anchor')

    document_text = document.GetText()
    document_end = len(document_text)

    selection_start, selection_end = shared.get_selection_unicode(editor)

    for _ in [0]:
        if _is_position_on_string(editor, selection_start):
            current_string_range = \
                             _find_string_from_position(editor, selection_start)
            if (selection_start, selection_end) == current_string_range:
                base_position = current_string_range[1] + 1
                if base_position > document_end:
                    return
            elif inner and 1 <= current_string_range[1] - selection_end <= 3 \
                 and 1 <= selection_start - current_string_range[0] <= 5 and \
                 document_text[selection_start - 1] in ('"', "'") and \
                 document_text[selection_end] in ('"', "'"):
                base_position = current_string_range[1] + 1
                if base_position > document_end:
                    return

            else:
                shared.set_selection_unicode(editor, *current_string_range)
                break
        else:
            base_position = selection_start

        for position in range(base_position, document_end+1):
            if _is_position_on_string(editor, position):
                string_range = _find_string_from_position(editor, position)
                shared.set_selection_unicode(editor, *string_range)
                break
        else:
            return

    if inner:
        _innerize_selected_string(editor)


def select_prev_string(inner=False):
    '''
    Select the previous string, starting from caret location.

    Provide `inner=True` to select only the contents of the string.

    Suggested key combinations: `Ctrl-Quotedbl`
                                `Alt-Quotedbl` for `inner=True`

    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    app.ExecuteCommand('set-visit-history-anchor')

    document_start = 0

    caret_position = shared.get_selection_unicode(editor)[1]

    for _ in [0]:

        if _is_position_on_string(editor, caret_position) or \
                      _is_position_on_string(editor, caret_position - 1):
            current_string_range = \
                              _find_string_from_position(editor, caret_position)
            base_position = current_string_range[0] - 1
            if base_position < document_start:
                return
        else:
            base_position = caret_position

        for position in range(base_position, document_start-1, -1):
            if _is_position_on_string(editor, position):
                string_range = _find_string_from_position(editor, position)
                shared.set_selection_unicode(editor, *string_range)
                break
        else:
            return

    if inner:
        _innerize_selected_string(editor)


string_pattern = re.compile(
    '''^(?P<prefix>[uUbBrRfF]*)(?P<delimiter>(\''')|(""")|(')|(")).*$''',
    flags=re.DOTALL
)

def _innerize_selected_string(editor):
    '''Given that a string is selected, select only its contents.'''
    assert isinstance(editor, wingapi.CAPIEditor)
    selection_start, selection_end = shared.get_selection_unicode(editor)
    document_string = shared.get_text(editor.GetDocument())
    string = document_string[selection_start:selection_end]
    match = string_pattern.match(string)
    if not match:
        # This happens on f-strings because our code doesn't support them well enough. If it does,
        # let's give up on innerizing and not show an exception.
        return
    delimiter = match.group('delimiter')
    prefix = match.group('prefix')
    fixed_start = selection_start + len(delimiter) + len(prefix)
    fixed_end = selection_end - len(delimiter) if string.endswith(delimiter) \
                                                             else selection_end
    shared.set_selection_unicode(editor, fixed_start, fixed_end)

