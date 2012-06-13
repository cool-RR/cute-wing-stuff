# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import collections
import inspect

import wingapi

import shared


class FileKind(type):
    ''' '''
        
class BaseFile(object):
    ''' '''
    __metaclass__ = FileKind
    
class ViewFile(BaseFile):
    ''' '''
    
class FormFile(BaseFile):
    ''' '''
    
class TemplateFile(BaseFile):
    ''' '''
    
Trinity = collections.namedtuple('trinity',
                                 'view_file template_file form_file',
                                 verbose=True)

trinities = []

def _find_trinity(file_path):
    ''' '''
    for trinity in trinities:
        if (trinity.view_file == file_path) or \
           (trinity.template_file == file_path) or \
                                              (trinity.form_file == file_path):
            return trinity
    else:
        return None
    
    
def _identify_file_kind(editor):
    ''' '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    filename = document.GetFilename()
    if filename.endswith('.html'):
        return TemplateFile
    elif filename.endswith('_form.py'):
        return FormFile
    elif filename.endswith('_view.py'):
        return ViewFile
    else:
        return None
    
        

def switch_to_form(editor=wingapi.kArgEditor):
    ''' '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    
    file_path = document.GetFilename()
    file_kind = _identify_file_kind(editor)
    if not file_kind:
        return
    I WAS HERE
    

#def comment_hr(editor=wingapi.kArgEditor):
    #'''
    #Enter a horizontal line of "#" characters going until character 79.
    
    #Example:
    
        ########################################################################
        
    #'''
    
    #assert isinstance(editor, wingapi.CAPIEditor)
    
    #document = editor.GetDocument()
    #assert isinstance(document, wingapi.CAPIDocument)
    
    #with shared.UndoableAction(document):
        
        #original_start, original_end = editor.GetSelection()
        #original_end_line_number = \
                #document.GetLineNumberFromPosition(original_end)
        #original_document_length = document.GetLength()
        #original_line_count = document.GetLineCount()
        
        #indent_size = shared.get_indent_size_in_pos(editor, original_start)

        #string_to_write = (' ' * indent_size) + ('#' * (79 - indent_size)) + \
                                                                           #'\n'
        
        #assert len(string_to_write) == 79
        
        #start_line_number = document.GetLineNumberFromPosition(original_start)
        #start_line_first_char = document.GetLineStart(start_line_number)
        #document.InsertChars(start_line_first_char, string_to_write)

        #editor.ExecuteCommand('home')