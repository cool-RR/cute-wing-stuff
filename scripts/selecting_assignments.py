# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines scripts for selecting parts of assignments.

See its documentation for more information.
'''

from __future__ import with_statement

import re
import bisect

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import wingapi

import shared

    
assignment_pattern = re.compile(
    r'''(?<=\n)(?P<indent>[ \t]*)''' # Before LHS
    
    # LHS:
    r'''(?P<lhs>(?!if |while |elif |assert )[^ \n][^=\n\(]*?)'''
    
    r''' +(?:[+\-*/%|&^]|<<|>>|//|\*\*)?= +''' # operator and padding
    
    # RHS:
    r'''(?P<rhs>[^ ][^\n]*\n''' 
    r'''(?:(?:[ \t]*[)\]}][^\n]*[\n])|(?:(?=(?P=indent)[ \t])[^\n]*\n))*)'''
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
    stripper = lambda (start, end): \
        shared.strip_segment_from_whitespace_and_newlines(document_text,
                                                          start, end)
    return map(stripper, (match.span('rhs') for match in matches))


###############################################################################


def select_next_lhs(editor=wingapi.kArgEditor, app=wingapi.kArgApplication):
    '''
    Select the next left-hand-side of an assignment.
    
    Suggested key combination: `Ctrl-Alt-9`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    _, position = editor.GetSelection()
    position += 1

    lhs_positions = _get_lhs_positions(editor.GetDocument())
    lhs_ends = tuple(lhs_position[1] for lhs_position in lhs_positions)
    lhs_index = bisect.bisect_left(lhs_ends, position)
    
    if 0 <= lhs_index < len(lhs_ends):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*lhs_positions[lhs_index])
        

def select_prev_lhs(editor=wingapi.kArgEditor, app=wingapi.kArgApplication):
    '''
    Select the previous left-hand-side of an assignment.
    
    Suggested key combination: `Ctrl-Alt-Parenleft`
    '''    
    assert isinstance(editor, wingapi.CAPIEditor)
    position, _ = editor.GetSelection()
    position -= 1

    lhs_positions = _get_lhs_positions(editor.GetDocument())
    lhs_starts = tuple(lhs_position[0] for lhs_position in lhs_positions)
    lhs_index = bisect.bisect_left(lhs_starts, position) - 1
    
    if 0 <= lhs_index < len(lhs_starts):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*lhs_positions[lhs_index])


def select_next_rhs(editor=wingapi.kArgEditor, app=wingapi.kArgApplication):
    '''
    Select the next right-hand-side of an assignment.
    
    Suggested key combination: `Ctrl-Alt-0`
    '''    
    assert isinstance(editor, wingapi.CAPIEditor)
    _, position = editor.GetSelection()
    position += 1

    rhs_positions = _get_rhs_positions(editor.GetDocument())
    rhs_ends = tuple(rhs_position[1] for rhs_position in rhs_positions)
    rhs_index = bisect.bisect_left(rhs_ends, position)
    
    if 0 <= rhs_index < len(rhs_ends):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*rhs_positions[rhs_index])
        

def select_prev_rhs(editor=wingapi.kArgEditor, app=wingapi.kArgApplication):
    '''
    Select the previous right-hand-side of an assignment.
    
    Suggested key combination: `Ctrl-Alt-Parenright`
    '''    
    assert isinstance(editor, wingapi.CAPIEditor)
    position, _ = editor.GetSelection()
    position -= 1

    rhs_positions = _get_rhs_positions(editor.GetDocument())
    rhs_starts = tuple(rhs_position[0] for rhs_position in rhs_positions)
    rhs_index = bisect.bisect_left(rhs_starts, position) - 1
    
    if 0 <= rhs_index < len(rhs_starts):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*rhs_positions[rhs_index])

