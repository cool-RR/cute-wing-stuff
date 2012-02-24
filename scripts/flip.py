# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `flip` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared

flip_pairs = (
    ('True', 'False'), 
)


def flip(editor=wingapi.kArgEditor):
    '''Flip between `True` and `False`.'''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    
    with shared.UndoableAction(document):
        start, end = shared.select_current_word(editor)
        word = document.GetCharRange(start, end)
        
        new_word = None
        for first_word, second_word in flip_pairs:
            if first_word == word:
                new_word = second_word
                break
            elif second_word == word:
                new_word = first_word
                break
            else:
                continue
            
        if new_word:
            document.DeleteChars(start, end-1)
            document.InsertChars(start, new_word)
            editor.SetSelection(start + len(new_word),
                                start + len(new_word))
        
            
