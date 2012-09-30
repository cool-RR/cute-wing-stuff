# This program is distributed under the MIT license.
# Copyright 2009-2012 Ram Rachum.

'''
This module defines the `previous_brace_match` script.

See its documentation for more information.
'''

from __future__ import with_statement

import _ast

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared

            
def previous_brace_match(editor=wingapi.kArgEditor):
    '''
    Select the previous pair of braces.
    
    Similar to Wing's built-in `brace-match`, except it goes backwards instead
    of going forwards. Goes to the nearest pair of braces, whether it's (), [],
    or {} that's before the current caret position, and selects those braces
    including all their content.
    
    Known limitation: Doesn't know to ignore braces found in strings.
    
    Suggested key combination: `Ctrl-Bracketleft`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    document_text = document.GetText()
    _, caret_position = editor.GetSelection()
    closing_brace_position = max((
        document_text.rfind(')', 0, caret_position - 1), 
        document_text.rfind(']', 0, caret_position - 1), 
        document_text.rfind('}', 0, caret_position - 1)
    ))
    print(closing_brace_position)
    if closing_brace_position == -1:
        return
    new_position = closing_brace_position
    editor.SetSelection(new_position, new_position)
    editor.ExecuteCommand('brace-match')