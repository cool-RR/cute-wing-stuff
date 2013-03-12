# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `direct_to_get` script.

See its documentation for more information.
'''


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import re
import inspect

import wingapi

import shared


caret_token = 'mUwMzJiNDg3MGE4NGE0ZmFjZGJkMGQ2NTNlNGQ4ZjQ5YTZjMGI1YzYwMmY0YjUw'

pattern = re.compile(
    r'''.*?(?P<square_brackets>\[(?P<key_head>[^\]]*)'''
    r'''%s(?P<key_tail>[^\]]*)\]).*''' % caret_token
)

def dict_direct_to_get(editor=wingapi.kArgEditor):
    '''
    Suggested key combination: 
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    
    _, current_position = editor.GetSelection()
    current_line_number = document.GetLineNumberFromPosition(current_position)
    line_start = document.GetLineStart(current_line_number)
    line_end = document.GetLineEnd(current_line_number)
    pimped_line_text = ''.join(line_start,
                               caret_token,
                               line_end)
    
    match = pattern.match(pimped_line_text)
    if not match:
        return
    else: # we have a match
        
    
    with shared.UndoableAction(document):
        start, end = shared.select_current_word(editor)    
        variable_name = document.GetCharRange(start, end)
        result_string = 'self.%s = %s' % (variable_name, variable_name)
        document.DeleteChars(start, end - 1)
        document.InsertChars(start, result_string)
        editor.SetSelection(start + len(result_string),
                            start + len(result_string))
        editor.ExecuteCommand('new-line')
    
        
