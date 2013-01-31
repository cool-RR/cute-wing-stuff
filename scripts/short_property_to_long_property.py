# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `short_property_to_long_property` script.

See its documentation for more information.
'''

from __future__ import division
from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


#propertoids = ('property', 'CachedProperty', 'caching.CachedProperty')
    
def short_property_to_long_property(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    
    _, caret = editor.GetSelection()
    document_text = document.GetText()
    property_position = document_text.rfind('property', 0, caret)
    if property_position == -1:
        return
    
    with shared.UndoableAction(document):
        editor.SetSelection(property_position + 1, property_position + 1)
        editor.ExecuteCommand('select-statement')