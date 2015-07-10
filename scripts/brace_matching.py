# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import _ast

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import wingapi

import shared

            
def brace_match_inner(editor=wingapi.kArgEditor):
    '''
    Select the inside of the current/next pair of braces.
    
    Similar to Wing's built-in `brace-match`, except it selects only the inside
    of the braces, not including the braces themselves.
    
    Known limitations: Misses some pairs of braces. Doesn't know to ignore
    braces found in strings.
    
    Suggested key combination: `Alt-Bracketright`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    editor.SetSelection(editor.GetSelection()[0]-1, editor.GetSelection()[1]+1)
    editor.ExecuteCommand('brace-match')
    editor.SetSelection(editor.GetSelection()[0]+1, editor.GetSelection()[1]-1)
    
    
def previous_brace_match(editor=wingapi.kArgEditor):
    '''
    Select the previous pair of braces.
    
    Similar to Wing's built-in `brace-match`, except it goes backwards instead
    of going forwards. Goes to the nearest pair of braces, whether it's (), [],
    or {} that's before the current caret position, and selects those braces
    including all their content.
    
    Known limitations: Misses some pairs of braces. Doesn't know to ignore
    braces found in strings.
    
    Suggested key combination: `Ctrl-Bracketleft`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    document_text = shared.get_text(document)
    _, caret_position = editor.GetSelection()
    closing_brace_position = max((
        document_text.rfind(')', 0, caret_position - 1), 
        document_text.rfind(']', 0, caret_position - 1), 
        document_text.rfind('}', 0, caret_position - 1)
    ))
    if closing_brace_position == -1:
        return
    new_position = closing_brace_position
    editor.SetSelection(new_position, new_position)
    editor.ExecuteCommand('brace-match')

    
def previous_brace_match_inner(editor=wingapi.kArgEditor):
    '''
    Select the inside of the previous pair of braces.
    
    Similar to Wing's built-in `brace-match`, except it goes backwards instead
    of going forwards. Goes to the nearest pair of braces, whether it's (), [],
    or {} that's before the current caret position, and selects the content of
    those braces, not including the braces themselves.
    
    Known limitations: Misses some pairs of braces. Doesn't know to ignore
    braces found in strings.
    
    Suggested key combination: `Alt-Bracketleft`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    
    editor.SetSelection(editor.GetSelection()[0]+1, editor.GetSelection()[1]-1)
    previous_brace_match(editor)
    editor.SetSelection(editor.GetSelection()[0]+1, editor.GetSelection()[1]-1)