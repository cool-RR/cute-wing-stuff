# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `cute_evaluate_sel_in_debug_probe` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def cute_evaluate_sel_in_debug_probe(editor=wingapi.kArgEditor):
    '''
    Evaluate selection in debug probe, do `select-more` if no selection.

    Suggested key combination: `Ctrl-Alt-D`
    '''
    
    assert isinstance(editor, wingapi.CAPIEditor)
    selection_start, selection_end = editor.GetSelection()
    if selection_start == selection_end:
        editor.ExecuteCommand('select-more')
    
    wingapi.gApplication.ExecuteCommand('evaluate-sel-in-debug-probe')