# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `for_thing_in_things` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import re

import wingapi

import shared


plural_pattern = re.compile('^(.*?s)$')
django_model_pattern('^.*[ .]([A-Z].*?s)\.(filter|all|exclude)\(.*\)s$')



def for_thing_in_things(editor=wingapi.kArgEditor):
    '''
    Turn `things` into `for thing in things:`.
    
    Type any pluarl word, like `bananas` or `directories`. Then run this
    script, and you get `for directory in directories`.
    
    Note: The `:` part is added only on Windows.
    
    Suggested key combination: `Insert Ctrl-F`
    '''
    
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    
    assert isinstance(document, wingapi.CAPIDocument)
    
    with shared.UndoableAction(document):
        
        editor.ExecuteCommand('end-of-line')
        end_position, _ = editor.GetSelection()
        editor.ExecuteCommand('beginning-of-line-text')
        start_position, _ = editor.GetSelection()
        base_text = document.GetCharRange(start_position, end_position)
        if not plural_word.endswith('s'):
            return
        singular_word = shared.plural_word_to_singular_word(plural_word)
        
        segment_to_insert = 'for %s in ' % singular_word
        editor.ExecuteCommand('beginning-of-line-text')
        current_position, _ = editor.GetSelection()
        document.InsertChars(current_position, segment_to_insert)
        editor.ExecuteCommand('end-of-line')
        
        if shared.autopy_available:
            import autopy.key
            autopy.key.tap(':')        