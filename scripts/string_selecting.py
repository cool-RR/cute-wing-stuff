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


def is_position_on_strict_string(editor, position):
    '''
    Is there a strict string in the specified position in the document?
    
    "Strict" here means that it's a string and it's *not* the last character of
    the string.
    '''
    return editor.fEditor.GetCharType(position) == edit.editor.kStringCharType


def find_string_from_position(editor, position):
    '''
    Given a character in the document known to be in a string, find its string.
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    assert is_position_on_strict_string(editor, position)
    document_start = 0
    document_end = editor.GetDocument().GetLength()
    start_marker = end_marker = position
    while end_marker < document_end and \
                            is_position_on_strict_string(editor, end_marker+1):
        end_marker += 1
    while start_marker > document_start and \
                          is_position_on_strict_string(editor, start_marker-1):
        start_marker -= 1
            
    if start_marker > document_start:
        assert not is_position_on_strict_string(editor, start_marker-1)
    if end_marker < document_end:
        assert not is_position_on_strict_string(editor, end_marker+1)

    return (start_marker, end_marker + 1)
            
            
def select_next_string(inner=False, editor=wingapi.kArgEditor,
                       app=wingapi.kArgApplication):
    '''
    Select the next (or current) string, starting from caret location.
    
    Provide `inner=True` to select only the contents of the string.
    
    Suggested key combinations: `Ctrl-Apostrophe`
                                `Alt-Apostrophe` for `inner=True`

    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    app.ExecuteCommand('set-visit-history-anchor')

    document_start = 0
    document_end = document.GetLength()
    
    selection_start, selection_end = editor.GetSelection()
    
    for _ in [0]:
        if is_position_on_strict_string(editor, selection_start):
            current_string_range = \
                             find_string_from_position(editor, selection_start)
            if (selection_start, selection_end) == current_string_range:
                base_position = current_string_range[1] + 1
                if base_position > document_end:
                    return
            elif inner and 1 <= current_string_range[1] - selection_end <= 3 \
                 and 1 <= selection_start - current_string_range[0] <= 5 and \
                 document.GetCharRange(selection_start-1,
                                       selection_start) in ('"', "'") and \
                 document.GetCharRange(selection_end,
                                       selection_end+1) in ('"', "'"):
                base_position = current_string_range[1] + 1
                if base_position > document_end:
                    return                
            
            else:
                editor.SetSelection(*current_string_range)
                break
        else:
            base_position = selection_start
    
        for position in range(base_position, document_end+1):
            if is_position_on_strict_string(editor, position):
                string_range = find_string_from_position(editor, position)
                editor.SetSelection(*string_range)
                break
        else:
            return
    
    if inner:
        _innerize_selected_string(editor)
    
    
def select_prev_string(inner=False, editor=wingapi.kArgEditor,
                       app=wingapi.kArgApplication):
    '''
    Select the previous string, starting from caret location.
    
    Provide `inner=True` to select only the contents of the string.
    
    Suggested key combinations: `Ctrl-Quotedbl`
                                `Alt-Quotedbl` for `inner=True`

    '''    
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    app.ExecuteCommand('set-visit-history-anchor')

    document_start = 0
    document_end = document.GetLength()
    
    caret_position = editor.GetSelection()[1]

    for _ in [0]:
            
        if is_position_on_strict_string(editor, caret_position) or \
                      is_position_on_strict_string(editor, caret_position - 1):
            current_string_range = \
                              find_string_from_position(editor, caret_position)
            base_position = current_string_range[0] - 1
            if base_position < document_start:
                return
        else:
            base_position = caret_position
    
        for position in range(base_position, document_start-1, -1):
            if is_position_on_strict_string(editor, position):
                string_range = find_string_from_position(editor, position)
                editor.SetSelection(*string_range)
                break
        else:
            return
    
    if inner:
        _innerize_selected_string(editor)
    

string_pattern = re.compile(
    '''^[urUR]{0,2}(?P<delimiter>(\''')|(""")|(')|(")).*$''',
    flags=re.DOTALL
)

def _innerize_selected_string(editor):
    '''Given that a string is selected, select only its contents.'''
    assert isinstance(editor, wingapi.CAPIEditor)
    selection_start, selection_end = editor.GetSelection()
    string = editor.GetDocument().GetCharRange(selection_start, selection_end)
    match = string_pattern.match(string)
    assert match
    delimiter = match.group('delimiter')
    fixed_start = selection_start + len(delimiter)
    fixed_end = selection_end - len(delimiter) if string.endswith(delimiter) \
                                                             else selection_end
    editor.SetSelection(fixed_start, fixed_end)                               
        
    
def say_char_type(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    print(editor.fEditor.GetCharType(editor.GetSelection()[0]))