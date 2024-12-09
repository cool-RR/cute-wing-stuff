# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines CamelCase-selecting scripts.

See their documentation for more information.
'''

from __future__ import with_statement

import re
import _ast

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import wingapi
import edit

import shared


camelcase_pattern = re.compile(
    r'''(?:[a-zA-Z_]*[a-z]+[a-zA-Z0-9_]*[A-Z]+[a-zA-Z0-9_]*)'''
    r'''|'''
    r'''(?:[a-zA-Z_]*[A-Z]+[a-zA-Z0-9_]*[a-z]+[a-zA-Z0-9_]*)'''
)


def _get_all_camelcase_positions(editor):
    text = shared.get_text(editor.GetDocument())
    matches = tuple(camelcase_pattern.finditer(text))
    return tuple((match.start(), match.end()) for match in matches)


def _get_relevant_camelcase_positions(editor, caret_position):
    assert isinstance(editor, wingapi.CAPIEditor)
    all_camelcase_positions = _get_all_camelcase_positions(editor)
    last_start_position = last_end_position = None
    for i, (start_position, end_position) in \
                                            enumerate(all_camelcase_positions):
        if end_position >= caret_position:
            next_start_position, next_end_position = \
                                                   start_position, end_position
            break
        else:
            last_start_position, last_end_position = \
                                                   start_position, end_position
    else:
        next_start_position = next_end_position = None
    return ((last_start_position, last_end_position),
            (next_start_position, next_end_position))


def select_next_camelcase():
    '''
    Select the next (or current) camelcase in the document.

    Camelcase means a variable name that has a combination of lowercase and
    uppercase letters.

    Suggested key combination: `Ctrl-Alt-C`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    caret_position = shared.get_selection_unicode(editor)[1] + 1

    _, next_camelcase_position = \
                      _get_relevant_camelcase_positions(editor, caret_position)
    if next_camelcase_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *next_camelcase_position)


def select_prev_camelcase():
    '''
    Select the previous camelcase in the document.

    Camelcase means a variable name that has a combination of lowercase and
    uppercase letters.

    Suggested key combination: `Ctrl-Alt-Shift-C`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    caret_position = shared.get_selection_unicode(editor)[0]

    prev_camelcase_position, _  = \
                      _get_relevant_camelcase_positions(editor, caret_position)
    if prev_camelcase_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *prev_camelcase_position)
