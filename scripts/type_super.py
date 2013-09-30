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
    selection = editor.GetSelection()
    document.DeleteChars(*selection)
    document.InsertChars(selection[0], super_text)
    editor.SetSelection(selection[0]+len(super_text),
                        selection[0]+len(super_text))
    if shared.autopy_available:
        import autopy.key
        autopy.key.toggle(autopy.key.K_META, False)
        autopy.key.toggle(autopy.key.K_CONTROL, False)
        autopy.key.toggle(autopy.key.K_ALT, False)
        autopy.key.toggle(autopy.key.K_SHIFT, False)
        autopy.key.tap('(', autopy.key.MOD_SHIFT)    
