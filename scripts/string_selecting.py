# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines string-selecting scripts.

See its documentation for more information.
'''

from __future__ import with_statement

import re
import sys
import _ast
import string

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]

import wingapi
import edit

import shared


def _is_position_on_string(editor, position):
    '''Is there a string in the specified position in the document?'''
    token, _ = shared.get_token_and_span_for_position(editor, position)
    return bool(shared.string_pattern.match(token))


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
        token, span = shared.get_token_and_span_for_position(editor, position)
        if shared.string_pattern.match(token):
            current_string_range = span
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
            token, span = \
                       shared.get_token_and_span_for_position(editor, position)
            if shared.string_pattern.match(token):
                editor.SetSelection(*span)
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
            
        if _is_position_on_string(editor, caret_position) or \
                      _is_position_on_string(editor, caret_position - 1):
            current_string_range = \
                              _find_string_from_position(editor, caret_position)
            base_position = current_string_range[0] - 1
            if base_position < document_start:
                return
        else:
            base_position = caret_position
    
        for position in range(base_position, document_start-1, -1):
            if _is_position_on_string(editor, position):
                string_range = _find_string_from_position(editor, position)
                editor.SetSelection(*string_range)
                break
        else:
            return
    
    if inner:
        _innerize_selected_string(editor)
    


def _innerize_selected_string(editor):
    '''Given that a string is selected, select only its contents.'''
    assert isinstance(editor, wingapi.CAPIEditor)
    selection_start, selection_end = editor.GetSelection()
    string = editor.GetDocument().GetCharRange(selection_start, selection_end)
    match = shared.string_pattern.match(string)
    assert match
    delimiter = match.group('delimiter')
    prefix = match.group('prefix')
    fixed_start = selection_start + len(delimiter) + len(prefix)
    fixed_end = selection_end - len(delimiter) if string.endswith(delimiter) \
                                                             else selection_end
    editor.SetSelection(fixed_start, fixed_end)                               
        
def fok():
    document = wingapi.gApplication.GetActiveDocument()
    analysis = wingapi.gApplication.GetAnalysis(document.GetFilename())
    sys.foolog(analysis)
    sys.foolog(vars(analysis))
    