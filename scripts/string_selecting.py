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

import shared

            
def select_next_string(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    
    base_position = editor.GetSelection()[1] - 1
    
    next_quote_location = 
    
    editor.SetSelection(editor.GetSelection()[0]-1, editor.GetSelection()[1]+1)
    editor.ExecuteCommand('brace-match')
    editor.SetSelection(editor.GetSelection()[0]+1, editor.GetSelection()[1]-1)