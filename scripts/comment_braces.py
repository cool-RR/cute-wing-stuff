from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import inspect

import wingapi

import shared


def _decapitalize(string):
    if not string:
        return string
    return string[0].lower + string[0:]


def _get_indent_size_in_pos(editor, pos):
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    
    with shared.SelectionRestorer(editor):
        line_number = document.GetLineNumberFromPosition(pos)
        line_start_pos = document.GetLineStart(line_number)
        editor.SetSelection(pos, pos)
        editor.ExecuteCommand('tab-key')
        line_text_start_pos = editor.GetSelection()[0]
        
        return line_text_start_pos - line_start_pos
    


def comment_braces(title, editor=wingapi.kArgEditor):
    assert isinstance(title, basestring)
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    with shared.UndoableAction(document):
        original_start, original_end = editor.GetSelection()
        original_document_length = document.GetLength()
        indent_size = _get_indent_size_in_pos(original_start)
        
        if title:
            raw_start_title = (' %s: ' % title.capitalize())
            raw_end_title = (' Finished %s. ' % _decapitalize(title)
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
            (' ' * indent_size) + '#' + (' ' * (79 - indent_size - 2)) + '#'
        
        start_line_number = document.GetLineNumberFromPosition(original_start)
        start_line_first_char = document.GetLineStart(start_line_number)
        document.InsertChars(start_line_first_char, start_title + tips_string)
        
        new_end = original_end + (document.GetLength() - original_document_length)
        
        
        editor.ExecuteCommand('beginning-of-screen-line-text')
        
        variable_name = document.GetCharRange(start, end)
        result_string = 'self.%s = %s' % (variable_name, variable_name)
        document.DeleteChars(start, end - 1)
        document.InsertChars(start, result_string)
        editor.SetSelection(start + len(result_string),
                            start + len(result_string))
        editor.ExecuteCommand('new-line')
    
        
