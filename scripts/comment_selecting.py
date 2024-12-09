# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines comment-selecting scripts.

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

def _is_position_on_comment(editor, position, try_previous=True):
    '''Is there a comment in the specified position in the document?'''
    return (
        editor.fEditor.GetCharType(position) == edit.editor.kCommentCharType or
        (try_previous and position >= 1 and
         (editor.fEditor.GetCharType(position - 1) == edit.editor.kCommentCharType))
    )


def _find_comment_from_position(editor, position, multiline=False):
    '''
    Given a character in the document known to be in a comment, find its comment.
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    assert _is_position_on_comment(editor, position)
    document_start = 0
    document_end = editor.GetDocument().GetLength()
    start_marker = end_marker = position
    while end_marker < document_end and _is_position_on_comment(editor, end_marker+1):
        end_marker += 1
    while start_marker > document_start and _is_position_on_comment(editor, start_marker-1):
        start_marker -= 1

    if start_marker > document_start:
        assert not _is_position_on_comment(editor, start_marker-1)
    if end_marker < document_end:
        assert not _is_position_on_comment(editor, end_marker+1)

    if multiline:
        comment_ranges = [(start_marker, end_marker)]
        document_text = shared.get_text(editor.GetDocument())

        ### Scanning backward: ################################################
        #                                                                     #
        while True:
            start_of_first_comment = comment_ranges[0][0]
            # No backwards regex search in `re` yet, doing it manually:
            for i in range(start_of_first_comment - 1, 0, -1):
                if document_text[i] not in comment.whitespace:
                    candidate_end_of_additional_comment = i
                    print('Candidate: %s %s' % (i, document_text[i]))
                    break
            else:
                break

            if _is_position_on_comment(editor,
                       candidate_end_of_additional_comment, try_previous=False):
                comment_ranges.insert(
                    0,
                    _find_comment_from_position(
                        editor,
                        candidate_end_of_additional_comment
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
            end_of_last_comment = comment_ranges[-1][1]
            search_result = re.search('\S',
                                      document_text[end_of_last_comment:])
            if search_result:
                candidate_start_of_additional_comment = (end_of_last_comment +
                                                                            search_result.span()[0])
                if _is_position_on_comment(editor,
                                          candidate_start_of_additional_comment,
                                          try_previous=False):
                    comment_ranges.append(
                        _find_comment_from_position(
                            editor,
                            candidate_start_of_additional_comment
                        )
                    )
                    continue

            # (This is like an `else` clause for both the above `if`s.)
            return tuple(comment_ranges)
        #                                                                     #
        ### Finished scanning forward. ########################################


    else: # not multiline
        return (start_marker, end_marker)


def select_next_comment():
    '''
    Select the next (or current) comment, starting from caret location.

    Suggested key combinations: `Ctrl-Alt-3`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    app.ExecuteCommand('set-visit-history-anchor')

    document_start = 0
    document_end = document.GetLength()

    selection_start, selection_end = shared.get_selection_unicode(editor)

    for _ in [0]:
        if _is_position_on_comment(editor, selection_start):
            current_comment_range = \
                             _find_comment_from_position(editor, selection_start)
            if (selection_start, selection_end) == current_comment_range:
                base_position = current_comment_range[1] + 1
                if base_position > document_end:
                    return
            else:
                shared.set_selection_unicode(editor, *current_comment_range)
                break
        else:
            base_position = selection_start

        for position in range(base_position, document_end+1):
            if _is_position_on_comment(editor, position):
                comment_range = _find_comment_from_position(editor, position)
                shared.set_selection_unicode(editor, *comment_range)
                break
        else:
            return


def select_prev_comment():
    '''
    Select the previous comment, starting from caret location.

    Suggested key combinations: `Ctrl-Alt-Numbersign`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    app.ExecuteCommand('set-visit-history-anchor')

    document_start = 0
    document_end = document.GetLength()

    caret_position = shared.get_selection_unicode(editor)[1]

    for _ in [0]:

        if _is_position_on_comment(editor, caret_position) or \
                      _is_position_on_comment(editor, caret_position - 1):
            current_comment_range = \
                              _find_comment_from_position(editor, caret_position)
            base_position = current_comment_range[0] - 1
            if base_position < document_start:
                return
        else:
            base_position = caret_position

        for position in range(base_position, document_start-1, -1):
            if _is_position_on_comment(editor, position):
                comment_range = _find_comment_from_position(editor, position)
                shared.set_selection_unicode(editor, *comment_range)
                break
        else:
            return
