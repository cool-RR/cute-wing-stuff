# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `for_thing_in_things` script.

See its documentation for more information.
'''

from __future__ import with_statement

import re

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


range_pattern = re.compile('^range\(.*\)$')


def for_thing_in_things(editor=wingapi.kArgEditor):
    '''
    Turn `things` into `for thing in things:`.
    
    Type any pluarl word, like `bananas` or `directories`. Then run this
    script, and you get `for directory in directories`.
    
    This also works for making `range(number)` into `for i in range(number):`.
    
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
        
        ### Analyzing base text: ##############################################
        #                                                                     #
        if range_pattern.match(base_text):
            variable_name = 'i'
        elif base_text.endswith('s'):
            variable_name = shared.plural_word_to_singular_word(base_text)
        #                                                                     #
        ### Finished analyzing base text. #####################################
        
        segment_to_insert = 'for %s in ' % variable_name
        document.InsertChars(start_position, segment_to_insert)
        editor.ExecuteCommand('end-of-line')
        
        if shared.autopy_available:
            import autopy.key
            autopy.key.tap(':')        