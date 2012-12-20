# This program is distributed under the MIT license.
# Copyright 2009-2012 Ram Rachum.

'''
This module defines string-selecting scripts.

See its documentation for more information.
'''

from __future__ import with_statement

import _ast

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi
import edit

import shared


def is_position_on_string(editor, position):
    return editor.fEditor.GetCharType(position) == edit.editor.kStringCharType


def find_string_from_position(editor, position):
    assert isinstance(editor, wingapi.CAPIEditor)
    assert is_position_on_string(editor, position)
    document_start = 0
    document_end = editor.GetDocument().GetLength()
    start_marker = end_marker = position
    while end_marker < document_end:
        if is_position_on_string(editor, end_marker+1):
            end_marker += 1
    while start_marker > document_start:
        if is_position_on_string(editor, start_marker-1):
            start_marker -= 1
            
    if start_marker > document_start:
        assert not is_position_on_string(editor, start_marker-1)
    if end_marker < document_end:
        assert not is_position_on_string(editor, end_marker+1)
        
    
            
            
def select_next_string(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    
    _selection_start, _selection_end = editor.GetSelection()
    if _selection_start == _selection_end:
        base_position = _selection_end
    else:
        base_position = _selection_end - 1
        
    
    #next_quote_location = 
    
    #editor.SetSelection(editor.GetSelection()[0]-1, editor.GetSelection()[1]+1)
    #editor.ExecuteCommand('brace-match')
    #editor.SetSelection(editor.GetSelection()[0]+1, editor.GetSelection()[1]-1)