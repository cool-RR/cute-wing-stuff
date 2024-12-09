# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines constant-selecting scripts.

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


constant_pattern = re.compile(
    r'''(?<![A-Za-z0-9_])(?:_[0-9_]*)?(?:[A-Z][0-9_]*){2,}(?![A-Za-z0-9_])'''
)


def _get_all_constant_positions(editor):
    text = shared.get_text(editor.GetDocument())
    matches = tuple(constant_pattern.finditer(text))
    return tuple((match.start(), match.end()) for match in matches)


def _get_relevant_constant_positions(editor, caret_position):
    assert isinstance(editor, wingapi.CAPIEditor)
    all_constant_positions = _get_all_constant_positions(editor)
    last_start_position = last_end_position = None
    for i, (start_position, end_position) in enumerate(all_constant_positions):
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


def select_next_constant():
    '''
    Select the next (or current) constant in the document.

    Constant means a name in all caps, like DEBUG or LOGIN_REDIRECT_URL.

    Suggested key combination: `Ctrl-Alt-O`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    caret_position = shared.get_selection_unicode(editor)[1] + 1

    _, next_constant_position = _get_relevant_constant_positions(editor,
                                                            caret_position)
    if next_constant_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *next_constant_position)


def select_prev_constant():
    '''
    Select the previous constant in the document.

    Constant means a name in all caps, like DEBUG or LOGIN_REDIRECT_URL.

    Suggested key combination: `Ctrl-Alt-Shift-O`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    document = editor.GetDocument()

    caret_position = shared.get_selection_unicode(editor)[0]

    prev_constant_position, _  = _get_relevant_constant_positions(editor,
                                                             caret_position)
    if prev_constant_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *prev_constant_position)
