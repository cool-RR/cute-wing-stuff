# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines constant-selecting scripts.

See its documentation for more information.
'''

from __future__ import with_statement

import re
import _ast

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import wingapi
import edit

import shared


assignment_pattern = re.compile(
    r'''(?<!!|<|>|=)(?:\+|-|\*\*?|//?|%|\||\^|&|>>|<<)?=(?!=)'''
)
operator_pattern = re.compile(
    r'''(?:\+|-|\*\*?|//?|%|\||\^|&|>>|<<|~|==|!=|<|<=|>|>=)(?!=)'''
)


def _get_all_operator_positions(editor):
    text = shared.get_text(editor.GetDocument())
    matches = tuple(operator_pattern.finditer(text))
    return tuple((match.start(), match.end()) for match in matches)

def _get_all_assignment_positions(editor):
    text = shared.get_text(editor.GetDocument())
    matches = tuple(assignment_pattern.finditer(text))
    return tuple((match.start(), match.end()) for match in matches)


def _get_relevant_operator_positions(editor, caret_position):
    assert isinstance(editor, wingapi.CAPIEditor)
    all_operator_positions = _get_all_operator_positions(editor)
    last_start_position = last_end_position = None
    for i, (start_position, end_position) in enumerate(all_operator_positions):
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


def _get_relevant_assignment_positions(editor, caret_position):
    assert isinstance(editor, wingapi.CAPIEditor)
    all_assignment_positions = _get_all_assignment_positions(editor)
    last_start_position = last_end_position = None
    for i, (start_position, end_position) in enumerate(all_assignment_positions):
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


def select_next_operator(editor=wingapi.kArgEditor,
                         app=wingapi.kArgApplication):
    '''
    Select the next (or current) operator in the document.
    
    Operators are:
    
        + - * / ** // % | & ^ << >> == != < <= > >=
    
    Suggested key combination: `Alt-Backslash`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    caret_position = editor.GetSelection()[1] + 1
    
    _, next_operator_position = \
                      _get_relevant_operator_positions(editor, caret_position)
    if next_operator_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*next_operator_position)

    
def select_prev_operator(editor=wingapi.kArgEditor,
                          app=wingapi.kArgApplication):
    '''
    Select the previous operator in the document.
    
    Operators are:
    
        + - * / ** // % | & ^ << >> == != < <= > >=
    
    Suggested key combination: `Alt-Bar`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    
    caret_position = editor.GetSelection()[0]
    
    prev_operator_position, _  = \
                      _get_relevant_operator_positions(editor, caret_position)
    if prev_operator_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*prev_operator_position)

    
def select_next_assignment(editor=wingapi.kArgEditor,
                         app=wingapi.kArgApplication):
    '''
    Select the next (or current) assignment in the document.
    
    This includes:
    
        = += -= *= /= **= //= %= |= &= ^= <<= >>=
    
    Suggested key combination: `Ctrl-Alt-Backslash`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    caret_position = editor.GetSelection()[1] + 1
    
    _, next_assignment_position = \
                      _get_relevant_assignment_positions(editor, caret_position)
    if next_assignment_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*next_assignment_position)

    
def select_prev_assignment(editor=wingapi.kArgEditor,
                          app=wingapi.kArgApplication):
    '''
    Select the previous assignment in the document.
    
    This includes:
    
        = += -= *= /= **= //= %= |= &= ^= <<= >>=

    Suggested key combination: `Ctrl-Alt-Bar`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    
    caret_position = editor.GetSelection()[0]
    
    prev_assignment_position, _  = \
                      _get_relevant_assignment_positions(editor, caret_position)
    if prev_assignment_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*prev_assignment_position)
    