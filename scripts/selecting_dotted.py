# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines scripts for selecting dotted names.

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


dotted_pattern = re.compile(
    r'''(?:(?:[a-zA-Z_][a-zA-Z_0-9]*)(?:\s|\\\n)*\.(?:\s|\\\n)*)+[a-zA-Z_][a-zA-Z_0-9]*'''
)


def _get_all_dotted_positions(editor):
    text = shared.get_text(editor.GetDocument())
    matches = tuple(dotted_pattern.finditer(text))
    return tuple((match.start(), match.end()) for match in matches)

def _get_relevant_dotted_positions(editor, caret_position):
    assert isinstance(editor, wingapi.CAPIEditor)
    all_dotted_positions = _get_all_dotted_positions(editor)
    last_start_position = last_end_position = None
    for i, (start_position, end_position) in enumerate(all_dotted_positions):
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


def select_next_dotted():
    '''
    Select the next (or current) dotted name in the document, like `foo.bar`.

    Suggested key combination: `Ctrl-D`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    caret_position = shared.get_selection_unicode(editor)[1] + 1

    _, next_dotted_position = \
                      _get_relevant_dotted_positions(editor, caret_position)
    if next_dotted_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *next_dotted_position)


def select_prev_dotted():
    '''
    Select the previous dotted name in the document, like `foo.bar`.

    Suggested key combination: `Ctrl-Shift-D`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    caret_position = shared.get_selection_unicode(editor)[0]

    prev_dotted_position, _  = \
                      _get_relevant_dotted_positions(editor, caret_position)
    if prev_dotted_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *prev_dotted_position)

