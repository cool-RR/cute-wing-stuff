# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `push_line_to_end` script. blocktododoc whole module

See its documentation for more information.
'''


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import inspect

import wingapi

import shared


def push_line_to_end(editor=wingapi.kArgEditor):
    '''
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    position, _ = editor.GetSelection()
    line = document.GetLineNumberFromPosition(position)
    line_start = document.GetLineStart(line)
    line_end = document.GetLineEnd(line)
    raise Exception((line_start, line_end))
    #with shared.UndoableAction(document):
        #start, end = shared.select_current_word(editor)    
        #variable_name = document.GetCharRange(start, end)
        #result_string = 'self.%s = %s' % (variable_name, variable_name)
        #document.DeleteChars(start, end - 1)
        #document.InsertChars(start, result_string)
        #editor.SetSelection(start + len(result_string),
                            #start + len(result_string))
        #editor.ExecuteCommand('new-line')
    
        
