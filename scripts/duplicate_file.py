# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path
import sys
import shutil

sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
]


import wingapi
import wingutils.datatype
import guiutils.formbuilder

import shared


def duplicate_file(new_file_name):
    '''
    Create a copy of the current file (in the same folder) and open it.

    If a filename with no extension will be entered, the same extension used
    for the original file will be used for the new file.

    Suggested key combination: `Insert Ctrl-D`
    '''
    app = wingapi.gApplication
    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    original_file_path = document.GetFilename()
    folder, original_file_name = os.path.split(original_file_path)
    if '.' in original_file_name and '.' not in new_file_name:
        new_file_name += '.%s' % original_file_name.rsplit('.')[-1]
    new_file_path = os.path.join(folder, new_file_name)

    shutil.copy(original_file_path, new_file_path)

    app.OpenEditor(new_file_path)



duplicate_file.arginfo = lambda: \
    {
        'new_file_name': wingapi.CArgInfo(
            label='New file name (can omit extension)',
            type=wingutils.datatype.CType(''),
            formlet=guiutils.formbuilder.CSmallTextGui(
                default=os.path.split(
                    wingapi.gApplication.GetActiveEditor().GetDocument().
                                                                  GetFilename()
                )[-1],
                select_on_focus=True
            ),
            doc=''
            ),
    }

_no_reload_scripts = True