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
    
    Suggested key combination: `Ctrl-Alt-8`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    _, position = editor.GetSelection()
    position += 1

    invocation_positions = get_invocation_positions(editor.GetDocument())
    invocation_ends = tuple(invocation_position[1] for invocation_position in
                            invocation_positions)
    invocation_index = bisect.bisect_left(invocation_ends, position)
    
    if 0 <= invocation_index < len(invocation_ends):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*invocation_positions[invocation_index])
        

def select_prev_invocation(editor=wingapi.kArgEditor,
                           app=wingapi.kArgApplication):
    '''
    Select the previous invocation.
    
    Suggested key combination: `Ctrl-Alt-Asterisk`
    '''    
    assert isinstance(editor, wingapi.CAPIEditor)
    position, _ = editor.GetSelection()
    position -= 1

    invocation_positions = get_invocation_positions(editor.GetDocument())
    invocation_starts = tuple(invocation_position[0] for invocation_position
                              in invocation_positions)
    invocation_index = bisect.bisect_left(invocation_starts, position) - 1
    
    if 0 <= invocation_index < len(invocation_starts):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*invocation_positions[invocation_index])


