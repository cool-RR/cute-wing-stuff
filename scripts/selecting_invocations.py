# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines scripts for selecting invocations.

See its documentation for more information.
'''

from __future__ import with_statement

import re
import bisect

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared

    
invocation_pattern = re.compile(
    r'''([A-Za-z_][A-Za-z_0-9]*) *\('''
)    
    

def _get_matches(document):
    assert isinstance(document, wingapi.CAPIDocument)
    document_text = shared.get_text(document)
    return tuple(invocation_pattern.finditer(document_text))

def get_invocation_positions(document):
    matches = _get_matches(document)
    return tuple(match.span(1) for match in matches)
    
###############################################################################


def select_next_invocation(editor=wingapi.kArgEditor,
                           app=wingapi.kArgApplication):
    '''
    Select the next invocation.
    
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


