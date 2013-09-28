# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import re
import os.path
import shutil

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi
import wingutils.datatype
import guiutils.formbuilder

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


template_name_pattern = re.compile(r'''template_name *= * ['"]([^'"]+)['"]''')
view_file_path_pattern = re.compile(r'''view.*py.?$''')


def django_switch_between_view_and_template():
    
    app = wingapi.gApplication
    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    project = app.GetProject()
    all_file_paths = project.GetAllFiles()
    document_text = shared.get_text(document)
    original_file_path = document.GetFilename()
    folder, file_name = os.path.split(original_file_path)
    
    
    if file_name.endswith('.py'):
        print('Is Python file')
        match = template_name_pattern.search(document_text)
        if match:
            print('Got match')            
            template_partial_file_path = match.group(1)
            matching_file_paths = [
                file_path for file_path in all_file_paths
                if template_partial_file_path in file_path.replace('\\', '/')
            ]
            if matching_file_paths:
                print('Got matching file path')            
                matching_file_path = matching_file_paths[0]
                app.OpenEditor(matching_file_path, raise_window=True)
    elif file_name.endswith('.html'):
        print('Is HTML file')
        all_view_file_paths = [
            file_path for file_path in all_file_paths
            if view_file_path_pattern.match(view_file_path_pattern)
        ]
        
        match = template_name_pattern.search(document_text)
        if match:
            print('Got match')            
            template_partial_file_path = match.group(1)
            if matching_file_paths:
                print('Got matching file path')            
                matching_file_path = matching_file_paths[0]
                app.OpenEditor(matching_file_path, raise_window=True)
            
        
    
    
