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


range_pattern = re.compile('^(x?range)\(.*\)$')


def for_thing_in_things(editor=wingapi.kArgEditor, app=wingapi.kArgApplication,
                        comprehension=False):
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
    
    document_text = shared.get_text(document)
    
    assert isinstance(document, wingapi.CAPIDocument)
    
    with shared.UndoableAction(document):
        end_position, _ = editor.GetSelection()
        line_number = document.GetLineNumberFromPosition(end_position)
        line_start = document.GetLineStart(line_number)
        line_end = document.GetLineEnd(line_number)
        line_contents = document.GetCharRange(line_start, line_end)
        editor.SetSelection(end_position, end_position)
        if ')' in document.GetCharRange(end_position - 1, end_position + 1) \
                                                 and 'range(' in line_contents:
            
            start_position = document_text.find('range(', line_start)
            if document_text[start_position - 1] == 'x':
                start_position -= 1
            end_position = document_text.find(
                ')',
                start_position,
                min((line_end, end_position + 1))
            ) + 1
        else:
            wingapi.gApplication.ExecuteCommand('backward-word')
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
        
        with shared.SelectionRestorer(editor):
            app.ExecuteCommand('beginning-of-line-text(toggle=False)')
            home_position, _ = editor.GetSelection()
            
        if comprehension:
            segment_to_insert = ' %s' % segment_to_insert
            document.InsertChars(start_position, segment_to_insert)
            editor.SetSelection(start_position, start_position)
        else:
            document.InsertChars(home_position, segment_to_insert)            
            editor.ExecuteCommand('end-of-line')        
            if shared.autopy_available:
                import autopy.key
                autopy.key.tap(':')