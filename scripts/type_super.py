# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import re
import sys
import os.path
import shutil

sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import wingapi
import wingutils.datatype
import guiutils.formbuilder

import shared


def type_super():
    '''
    Type `super(MyClass, self).my_method()`

    `MyClass` and `my_method` will be copied with the current class and method
    of the active scope.

    Suggested key combination: `Insert Ctrl-S`
    '''

    app = wingapi.gApplication
    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    current_source_scopes = app.GetCurrentSourceScopes()
    print(current_source_scopes)
    two_last_scopes = tuple(current_source_scopes[0][-2:])
    print(two_last_scopes)
    super_text = 'super(%s, self).%s' % two_last_scopes
    selection = shared.get_selection_unicode(editor)
    document.DeleteChars(*selection)
    document.InsertChars(selection[0], super_text)
    shared.set_selection_unicode(editor, selection[0]+len(super_text),
                        selection[0]+len(super_text))
    if shared.autopy_available:
        import autopy.key
        autopy.key.tap('(', [autopy.key.Modifier.SHIFT])
