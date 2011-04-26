# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `instanciate` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def instanciate(title):
    '''
    
    '''
    
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    
    assert isinstance(document, wingapi.CAPIDocument)
    
    with shared.UndoableAction(document):
        start, end = shared.select_current_word(editor)
        word = document.GetCharRange(start, end)
        
        if '_' in word:
            raise Exception("Must use `instanciate` when the current word is "
                            "the CamelCase class name. The current word is "
                            "`%s`, and it has an underscore in it, so it's "
                            "not CamelCase.")
        
        lower_case_word = shared.camel_case_to_lower_case(word)
        
        segment_to_insert = '%s = ' % lower_case_word
            
        
        #document.DeleteChars(start, end-1)
        document.InsertChars(start, )
        editor.SetSelection(start + len(new_word),
                            start + len(new_word))
        #editor.ExecuteCommand('new-line')
    
        
