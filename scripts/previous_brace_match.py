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
    blocktododoc
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    with shared.ScrollRestorer(editor):
        document_text = document.GetText()
        caret_position, _ = editor.GetSelection()
        closing_brace_position = max((
            document_text.find(')', 0, caret_position), 
            document_text.find(']', 0, caret_position), 
            document_text.find('}', 0, caret_position)
        ))
        if closing_brace_position == -1:
            return
        editor.SetSelection(closing_brace_position, closing_brace_position)
        editor.ExecuteCommand('brace-match')