# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines scripts for selecting parts of assignments.

See its documentation for more information.
'''

from __future__ import with_statement

import re
import bisect

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared

    
assignment_pattern = re.compile(
    r'''(?<=\n)(?P<indent>[ \t]*)''' # Before LHS
    
    # LHS:
    r'''(?P<lhs>(?!if |while |elif |assert )[^ \n][^=\n\(]+?)'''
    
    r''' *(?:[+\-*/%|&^]|<<|>>|//|\*\*)?= *''' # operator and padding
    
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
    return tuple(match.span('rhs') for match in matches)

def _get_lhs_starts_and_ends(document):
    lhs_positions = _get_lhs_positions(document)
    lhs_starts = tuple(lhs_position[0] for lhs_position in lhs_positions)    
    lhs_ends = tuple(lhs_position[1] for lhs_position in lhs_positions)
    return (lhs_starts, lhs_ends)

def _get_rhs_starts_and_ends(document):
    rhs_positions = _get_rhs_positions(document)
    rhs_starts = tuple(rhs_position[0] for rhs_position in rhs_positions)    
    rhs_ends = tuple(rhs_position[1] for rhs_position in rhs_positions)    
    return (rhs_starts, rhs_ends)    


###############################################################################


def select_next_lhs(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    _, position = editor.GetSelection()
    position += 1
    lhs_starts, lhs_ends = _get_lhs_starts_and_ends(document)
    
    lhs_index_start_candidate = bisect.bisect_left(lhs_starts, position)
    lhs_index_end_candidate = bisect.bisect_left(lhs_ends, position)
    
    if lhs_index_start_candidate < len(lhs_positions):
        lhs_start_candidate = lhs_starts[lhs_index_start_candidate]
    else:
        lhs_start_candidate = None
        
    if lhs_index_end_candidate < len(lhs_positions):
        lhs_end_candidate = lhs_ends[lhs_index_end_candidate]
    else:
        lhs_end_candidate = None
    
    ### Choosing which index to use: ##########################################
    #                                                                         #
    none_count = (lhs_start_candidate, lhs_end_candidate).count(None)
    if none_count == 2:
        return
    elif none_count == 1:
        if lhs_start_candidate is not None:
            index_to_use = lhs_index_start_candidate
        else:
            assert lhs_end_candidate is not None
            index_to_use = lhs_index_end_candidate
    else:
        assert none_count == 0
        if lhs_index_start_candidate
            
    if lhs_index < len(lhs_positions):
        editor.SetSelection(*lhs_positions[lhs_index])

    #                                                                         #
    ### Finished choosing which index to use. #################################

def select_prev_lhs():
    pass

def select_next_rhs():
    pass

def select_prev_rhs():
    pass
    
    