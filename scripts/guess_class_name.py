# Copyright 2009-2014 Ram Rachum.
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
    '''
    Guess the class name based on file name, and replace class name.
    
    Imagine you had a file `foo_manager.py` with a class `FooManager` defined
    in it, and you duplicated it, calling the new file `bar_grokker.py`. If you
    run `guess-class-name`, it'll replace all instances of `FooManager` in your
    new file to `BarGrokker`.
    
    (It finds the original class name by taking the first class defined in the
    file. If the file defined multiple classes, you might get the wrong
    results.)
    
    Suggested key combination: `Insert Ctrl-C`
    '''
    
    app = wingapi.gApplication
    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    file_name_without_extension = \
                        os.path.split(document.GetFilename())[-1].split('.')[0]
    
    guessed_class_name = \
                   shared.lower_case_to_camel_case(file_name_without_extension)
    
    document_text = shared.get_text(document)
    
    
    matches = tuple(re.finditer(existing_class_name_pattern, document_text))
    if not matches:
        return
    match = matches[-1]
    existing_class_name = match.group(1)
    
    n_occurrences = document_text.count(existing_class_name
                                        )
    with shared.SelectionRestorer(editor):
        with shared.UndoableAction(document):
            document.SetText(
                document_text.replace(existing_class_name, guessed_class_name)
            )
            
    app.SetStatusMessage('Replaced %s occurrences' % n_occurrences)
    