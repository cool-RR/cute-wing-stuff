# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import itertools
import re
import os.path
import shutil

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi
import wingutils.datatype
import guiutils.formbuilder

import shared


template_name_pattern = re.compile(r'''template_name *= * ['"]([^'"]+)['"]''')
view_file_path_pattern = re.compile(r'''view.*py.?$''')
shorten_template_file_path_pattern = re.compile(
    r'''^.*template[^/]*(/.*$)'''
)


def django_switch_between_view_and_template():
    
    app = wingapi.gApplication
    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    project = app.GetProject()
    all_file_paths = project.GetAllFiles()
    document_text = shared.get_text(document)
    file_path = document.GetFilename()
    folder, file_name = os.path.split(file_path)
    
    
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
        short_file_path = shorten_template_file_path_pattern.match(
                                         file_path.replace('\\', '/')).group(1)
        specifies_our_template_pattern = re.compile(
            r'''template_name *= * ['"]%s['"]''' % re.escape(short_file_path)
        )
        all_view_file_paths = [
            file_path for file_path in all_file_paths
            if view_file_path_pattern.match(file_path)
        ]
        print(all_view_file_paths)
            
        file_contents = itertools.imap(shared.get_file_content,
                                       all_view_file_paths)
        matching_file_paths_iterator = itertools.ifilter(
            lambda file_content:
                           specifies_our_template_pattern.search(file_content),
            file_contents
        )
        try:
            matching_file_path = next(matching_file_paths_iterator)
            print('Got match: %s' % matching_file_path)
        except StopIteration:
            return
        app.OpenEditor(matching_file_path, raise_window=True)
