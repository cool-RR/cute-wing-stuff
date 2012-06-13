# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `cute_select_more` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


SAFETY_LIMIT = 20


def cute_select_more(editor=wingapi.kArgEditor):
    
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    select_more = lambda: wingapi.gApplication.ExecuteCommand('select-more')

    select_more()
    for i in range(SAFETY_LIMIT):
        selection_start, _ = editor.GetSelection()
        if document.GetCharRange(selection_start-1, selection_start) == '.':
            select_more()
    