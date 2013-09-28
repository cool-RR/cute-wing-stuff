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


existing_class_name_pattern = re.compile(
    r'''\n *class +([^(:]+) *[(:]'''
)



def guess_class_name():
    
    app = wingapi.gApplication
    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    file_name_without_extension = \
                        os.path.split(document.GetFilename())[-1].split('.')[0]
    
    guessed_class_name = \
                   shared.lower_case_to_camel_case(file_name_without_extension)
    
    document_text = shared.get_text(document)
    
    
    match = existing_class_name_pattern.search(document_text)
    if not match:
        return
    existing_class_name = match.group(1)
    
    n_occurrences = document_text.count(existing_class_name
                                        )
    with shared.SelectionRestorer(editor):
        with shared.UndoableAction(document):
            document.SetText(
                document_text.replace(existing_class_name, guessed_class_name)
            )
            
    app.SetStatusMessage('Replaced %s occurrences' % n_occurrences)
    