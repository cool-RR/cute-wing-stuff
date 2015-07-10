# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import wingapi

import shared


def instantiate(editor=wingapi.kArgEditor):
    '''
    Write `my_class_name = MyClassName()`.
        
    This is used to quickly instantiate a class. Write your class name, like
    `CatNip`. It will usually be autocompleted. Then execute this script, and
    you'll have `cat_nip = CatNip()`, with the cursor positioned between the
    brackes.
    
    This saves a lot of typing, because normally you don't have autocompletion
    for the new instance name `cat_nip` because it doesn't exist yet.
    
    Note: The `()` part is added only on Windows.
    '''
    
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    
    assert isinstance(document, wingapi.CAPIDocument)
    
    with shared.UndoableAction(document):
        editor.ExecuteCommand('end-of-line')
        start, end = shared.select_current_word(editor)
        word = document.GetCharRange(start, end)
        
        if '_' in word:
            raise Exception("Must use `instantiate` when the current word is "
                            "the CamelCase class name. The current word is "
                            "`%s`, and it has an underscore in it, so it's "
                            "not CamelCase.")
        
        lower_case_word = shared.camel_case_to_lower_case(word)
        segment_to_insert = '%s = ' % lower_case_word
        editor.ExecuteCommand('beginning-of-line-text')
        current_position, _ = editor.GetSelection()
        document.InsertChars(current_position, segment_to_insert)
        editor.ExecuteCommand('end-of-line')
        
        if shared.autopy_available:
            import autopy.key
            autopy.key.tap('(', autopy.key.MOD_SHIFT)