# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines scripts for selecting parts of assignments.

See their documentation for more information.
'''

from __future__ import with_statement

import re
import bisect

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import wingapi

import shared


assignment_pattern = re.compile(
    r'''(?<=\n)(?P<indent>[ \t]*)''' # Before LHS

    # LHS:
    r'''(?P<lhs>(?!if |while |elif |assert )[^ \n][^=\n\(]*?)'''

    r''' +(?:[+\-*/%|&^]|<<|>>|//|\*\*)?= +''' # operator and padding

    # RHS:
    r'''(?P<rhs>[^ ][^\n]*(?:\n|$)'''
    r'''(?:(?:[ \t]*[)\]}][^\n]*[\n])|(?:(?=(?P=indent)'''
    r'''[ \t])[^\n]*(?:\n|$)))*)'''
)


def _get_matches(document):
    assert isinstance(document, wingapi.CAPIDocument)
    document_text = shared.get_text(document)
    return tuple(assignment_pattern.finditer(document_text))

def _get_lhs_positions(document):
    matches = _get_matches(document)
    return tuple(match.span('lhs') for match in matches)

def _get_rhs_positions(document):
    matches = _get_matches(document)
    document_text = shared.get_text(document)
    stripper = lambda start_and_end: \
        shared.strip_segment_from_whitespace_and_newlines(document_text,
                                                          *start_and_end)
    return tuple(map(stripper, (match.span('rhs') for match in matches)))


###############################################################################


def select_next_lhs():
    '''
    Select the next left-hand-side of an assignment.

    Suggested key combination: `Ctrl-Alt-9`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    _, position = shared.get_selection_unicode(editor)
    position += 1

    lhs_positions = _get_lhs_positions(editor.GetDocument())
    lhs_ends = tuple(lhs_position[1] for lhs_position in lhs_positions)
    lhs_index = bisect.bisect_left(lhs_ends, position)

    if 0 <= lhs_index < len(lhs_ends):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *lhs_positions[lhs_index])


def select_prev_lhs():
    '''
    Select the previous left-hand-side of an assignment.

    Suggested key combination: `Ctrl-Alt-Parenleft`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    position, _ = shared.get_selection_unicode(editor)
    position -= 1

    lhs_positions = _get_lhs_positions(editor.GetDocument())
    lhs_starts = tuple(lhs_position[0] for lhs_position in lhs_positions)
    lhs_index = bisect.bisect_left(lhs_starts, position) - 1

    if 0 <= lhs_index < len(lhs_starts):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *lhs_positions[lhs_index])


def select_next_rhs():
    '''
    Select the next right-hand-side of an assignment.

    Suggested key combination: `Ctrl-Alt-0`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    _, position = shared.get_selection_unicode(editor)
    position += 1

    rhs_positions = _get_rhs_positions(editor.GetDocument())
    rhs_ends = tuple(rhs_position[1] for rhs_position in rhs_positions)
    rhs_index = bisect.bisect_left(rhs_ends, position)

    if 0 <= rhs_index < len(rhs_ends):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *rhs_positions[rhs_index])


def select_prev_rhs():
    '''
    Select the previous right-hand-side of an assignment.

    Suggested key combination: `Ctrl-Alt-Parenright`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    position, _ = shared.get_selection_unicode(editor)
    position -= 1

    rhs_positions = _get_rhs_positions(editor.GetDocument())
    rhs_starts = tuple(rhs_position[0] for rhs_position in rhs_positions)
    rhs_index = bisect.bisect_left(rhs_starts, position) - 1

    if 0 <= rhs_index < len(rhs_starts):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *rhs_positions[rhs_index])

