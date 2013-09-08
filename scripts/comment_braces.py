# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `comment_braces` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import inspect

import wingapi

import shared


def _decapitalize(string):
    '''Decapitalize a string's first letter.'''
    if not string:
        return string
    return string[0].lower() + string[1:]


def _capitalize(string):
    '''Capitalize a string's first letter.'''
    if not string:
        return string
    return string[0].upper() + string[1:]


def comment_braces(title):
    '''
    Create "comment braces" with a title around a piece of code.
    
    For example, if you have this code:
    
        do_something()
        do_something_else()
        meow = frr + 7
        do_something_again()
        
    You can select it, then run the `comment_braces` script with a title of
    "doing inane stuff", to get this:
        
        ### Doing inane stuff: ################################################
        #                                                                     #
        do_something()
        do_something_else()
        meow = frr + 7
        do_something_again()
        #                                                                     #
        ### Finished doing inane stuff. #######################################
        
    (Don't try this inside a docstring, it works only in real code.)
    
    The title usually has a first word ending with "ing". Don't bother
    capitalizing the first letter or ending the sentence with any punctuation
    mark. You may also use an empty title to get a title-less comment line.

    Suggested key combination: `Insert B`
    '''
    
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)    
    
    assert isinstance(title, basestring)
    if title.endswith(':') or title.endswith('.'):
        title = title[:-1]
    
    with shared.UndoableAction(document):
        
        original_start, original_end = editor.GetSelection()
        original_end_line_number = \
                document.GetLineNumberFromPosition(original_end)
        original_document_length = document.GetLength()
        original_line_count = document.GetLineCount()
        
        indent_size = shared.get_indent_size_in_pos(editor, original_start)
        
        if title:
            raw_start_title = (' %s: ' % _capitalize(title))
            raw_end_title = (' Finished %s. ' % _decapitalize(title))
        else:
            assert title == ''
            raw_start_title = ''
            raw_end_title = ''
            
        start_title_head = (' ' * indent_size) + '###' + raw_start_title
        end_title_head = (' ' * indent_size) + '###' + raw_end_title
        
        start_title = \
            start_title_head + '#' * (79 - len(start_title_head)) + '\n'
        end_title = \
            end_title_head + '#' * (79 - len(end_title_head)) + '\n'        
        tips_string = \
            (' ' * indent_size) + '#' + (' ' * (79 - indent_size - 2)) + '#\n'
        
        start_line_number = document.GetLineNumberFromPosition(original_start)
        start_line_first_char = document.GetLineStart(start_line_number)
        document.InsertChars(start_line_first_char, start_title + tips_string)
        
        end_line_number = original_end_line_number + \
            (document.GetLineCount() - original_line_count) + 1
        end_line_first_char = document.GetLineStart(end_line_number)
        document.InsertChars(end_line_first_char, tips_string + end_title)
    
        
    