# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `implicit_getattr_to_explicit` script.

See its documentation for more information.
'''


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import re
import inspect
import logging

import wingapi

import shared

python_identifier_subpattern = r'''[a-zA-Z_][0-9a-zA-Z_]*'''

pattern = re.compile(
    r'''(?P<object>%s)\.(?P<attribute_name>%s)''' % (
        python_identifier_subpattern, python_identifier_subpattern
    )
)

def implicit_getattr_to_explicit(editor=wingapi.kArgEditor):
    '''
    
    Suggested key combination: `Insert Shift-G`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    
    
    _, current_position = editor.GetSelection()
    head = max(current_position - 100, 0)
    tail = min(current_position + 100, document.GetLength())
    
    text = document.GetCharRange(head, tail)
    
    matches = list(re.finditer(pattern, text))

    logging.error('Printing matches:')
    for match in matches:
        logging.error(match.string[match.start():match.end()])
        
    return
    
    #if ']' not in line_tail:
        ##print('''']' not in line_tail''')
        #return
    
    #first_closing_bracket_position = line_tail.find(']') + len(line_head) + \
                                                                     #line_start
    
    #text_until_closing_bracket = document.GetCharRange(
        #line_start,
        #first_closing_bracket_position + 1
    #)
    
    #match = pattern.match(text_until_closing_bracket)
    #if not match:
        ##print('''no match''')
        ##print('{{{%s}}}' % text_until_closing_bracket)
        #return
    #else: # we have a match
        #square_brackets_position = \
            #line_text.find(match.group('square_brackets'))
        #text_to_insert = '.get(%s, None)' % match.group('key')
        #new_line_text = line_text.replace(
            #match.group('square_brackets'), text_to_insert
        #)
        #none_start = line_start + square_brackets_position + \
                                                        #len(text_to_insert) - 5
        #none_end = line_start + square_brackets_position + \
                                                        #len(text_to_insert) - 1

        #with shared.UndoableAction(document):
            #document.DeleteChars(line_start, line_end - 1)
            ## The `- 1` above is necessary for \n-documents.
            #document.InsertChars(line_start, new_line_text)
            #editor.SetSelection(none_start, none_end)
    
        
