# This program is distributed under the MIT license.
# Copyright 2009-2012 Ram Rachum.

'''
This module defines number-selecting scripts.

See its documentation for more information.
'''

from __future__ import with_statement

import re
import _ast

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi
import edit

import shared


number_pattern = re.compile(r'''([0-9]+(\.[0-9]+)?)|(\.[0-9]+)''')


def get_all_number_positions(editor):
    text = editor.GetDocument().GetText()
    matches = tuple(number_pattern.finditer(text))
    return tuple((match.start(), match.end()) for match in matches)


def get_relevant_number_positions(editor, caret_position):
    assert isinstance(editor, wingapi.CAPIEditor)
    all_number_positions = get_all_number_positions(editor)
    last_start_position = last_end_position = None
    for i, (start_position, end_position) in enumerate(all_number_positions):
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


def select_next_number(editor=wingapi.kArgEditor,
                       app=wingapi.kArgApplication):
    '''
    Select the next (or current) number in the document.
    
    Suggested key combination: Ctrl-0
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    #document_start = 0
    #document_end = document.GetLength()
    
    #selection_start, selection_end = editor.GetSelection()
    
    #number_positions_in_document = get_number_positions_in_document()

    caret_position = editor.GetSelection()[1] + 1
    
    _, next_number_position = get_relevant_number_positions(editor,
                                                            caret_position)
    if next_number_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*next_number_position)

    
def select_prev_number(editor=wingapi.kArgEditor,
                       app=wingapi.kArgApplication):
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    #document_start = 0
    #document_end = document.GetLength()
    
    #selection_start, selection_end = editor.GetSelection()
    
    #number_positions_in_document = get_number_positions_in_document()
    
    caret_position = editor.GetSelection()[0]
    
    prev_number_position, _  = get_relevant_number_positions(editor,
                                                             caret_position)
    if prev_number_position != (None, None):
        app.ExecuteCommand('set-visit-history-anchor')
        editor.SetSelection(*prev_number_position)
    