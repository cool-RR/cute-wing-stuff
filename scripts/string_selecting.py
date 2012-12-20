# This program is distributed under the MIT license.
# Copyright 2009-2012 Ram Rachum.

'''
This module defines string-selecting scripts.

See its documentation for more information.
'''

from __future__ import with_statement

import re
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
    while end_marker < document_end and \
                                   is_position_on_string(editor, end_marker+1):
        end_marker += 1
    while start_marker > document_start and \
                                 is_position_on_string(editor, start_marker-1):
        start_marker -= 1
            
    if start_marker > document_start:
        assert not is_position_on_string(editor, start_marker-1)
    if end_marker < document_end:
        assert not is_position_on_string(editor, end_marker+1)

    return (start_marker, end_marker + 1)
            
            
def select_next_string(inner=False, editor=wingapi.kArgEditor,
                       app=wingapi.kArgApplication):
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    app.ExecuteCommand('set-visit-history-anchor')

    document_start = 0
    document_end = document.GetLength()
    
    #_selection_start, _selection_end = editor.GetSelection()
    #if _selection_start == _selection_end:
        #base_position = _selection_end
    #else:
        #base_position = _selection_end - 1
        
    caret_position = editor.GetSelection()[0]
    print('Caret position is %s' % caret_position)
    
    for _ in [0]:
        if is_position_on_string(editor, caret_position):
            current_string_range = \
                              find_string_from_position(editor, caret_position)
            if editor.GetSelection() == current_string_range:
                base_position = current_string_range[1] + 1
                if base_position > document_end:
                    return
            else:
                editor.SetSelection(*current_string_range)
                break
        else:
            base_position = caret_position
    
        print('Base position is %s' % base_position)
            
        for position in range(base_position, document_end+1):
            if is_position_on_string(editor, position):
                string_range = find_string_from_position(editor, position)
                editor.SetSelection(*string_range)
                break
        else:
            return
    
    if inner:
        _innerize_selected_string(editor)
    
    
def select_prev_string(editor=wingapi.kArgEditor, app=wingapi.kArgApplication):
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    app.ExecuteCommand('set-visit-history-anchor')

    document_start = 0
    document_end = document.GetLength()
    
    caret_position = editor.GetSelection()[1]

    print('Caret position is %s' % caret_position)

    for _ in [0]:
            
        if is_position_on_string(editor, caret_position) or \
                             is_position_on_string(editor, caret_position - 1):
            current_string_range = \
                              find_string_from_position(editor, caret_position)
            base_position = current_string_range[0] - 1
            if base_position < document_start:
                return
        else:
            base_position = caret_position
    
        print('Base position is %s' % base_position)
            
        for position in range(base_position, document_start-1, -1):
            if is_position_on_string(editor, position):
                string_range = find_string_from_position(editor, position)
                editor.SetSelection(*string_range)
                break
        else:
            return
    
    if inner:
        _innerize_selected_string(editor)
    

string_pattern = re.compile('''^[urUR]*('|"|\'''|""").*$''')

def _innerize_selected_string(editor):
    assert isinstance(editor, wingapi.CAPIEditor)
    selection_start, selection_end = editor.GetSelection()
    string = editor.GetDocument().GetCharRange(selection_start, selection_end)
    match = string_pattern.match(string)
    assert match
    quote = match.groups()
    fixed_start = selection_start + len(quote)
    fixed_end = selection_end - len(quote) if string.endswith(quote) else \
                                                                  selection_end
    editor.SetSelection(fixed_start, fixed_end)                               
        
    