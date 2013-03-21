# Copyright 2009-2013 Ram Rachum.
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


def for_thing_in_things(editor=wingapi.kArgEditor, comprehension=False):
    '''
    Turn `things` into `for thing in things:`.
    
    Type any pluarl word, like `bananas` or `directories`. Then run this
    script, and you get `for directory in directories`.
    
    This also works for making `range(number)` into `for i in range(number):`.
    
    Note: The `:` part is added only on Windows.
    
    If `comprehension=True`, inputs `for thing in things` without the colon and
    puts the caret before instead of after.
    
    Suggested key combination: `Insert Ctrl-F`
                               `Insert Shift-F` for `comprehension=True`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    
    assert isinstance(document, wingapi.CAPIDocument)
    
    with shared.UndoableAction(document):
        editor.ExecuteCommand('end-of-line')
        end_position, _ = editor.GetSelection()
        line_number = document.GetLineNumberFromPosition(end_position)
        line_start = document.GetLineStart(line_number)
        line_end = document.GetLineEnd(line_number)
        line_contents = document.GetCharRange(line_start, line_end)
        editor.SetSelection(end_position, end_position)
        if ')' in document.GetCharRange(end_position - 1, end_position + 1) \
                                                 and 'range(' in line_contents:
            
            start_position = document.GetText().find('range(', line_start)
        else:
            wingapi.gApplication.ExecuteCommand('backward-word')
            start_position, _ = editor.GetSelection()
            

        print(start_position, end_position)
        base_text = document.GetCharRange(start_position, end_position)
        print(base_text)
        ### Analyzing base text: ##############################################
        #                                                                     #
        if range_pattern.match(base_text):
            variable_name = 'i'
        elif base_text.endswith('s'):
            variable_name = shared.plural_word_to_singular_word(base_text)
        #                                                                     #
        ### Finished analyzing base text. #####################################
        
        segment_to_insert = 'for %s in ' % variable_name
        if comprehension:
            segment_to_insert = ' %s' % segment_to_insert
        document.InsertChars(start_position, segment_to_insert)
        
        if comprehension:
            editor.SetSelection(start_position, start_position)
        else:
            editor.ExecuteCommand('end-of-line')
        
            if shared.autopy_available:
                import autopy.key
                autopy.key.tap(':')        