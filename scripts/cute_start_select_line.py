# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `cute_start_select_line` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def cute_start_select_line(editor=wingapi.kArgEditor):
    '''

    Suggested key combination: `Ctrl-F8`
    '''
    
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    selection_start, selection_end = editor.GetSelection()
    selection_start_line = document.GetLineNumberFromPosition(selection_start)
    selection_end_line = document.GetLineNumberFromPosition(selection_end)
    new_selection_start = document.GetLineStart(selection_start_line)
    new_selection_end = document.GetLineEnd(selection_end_line)

    wingapi.gApplication.ExecuteCommand('start-select-line')
    editor.SetSelection(new_selection_start, new_selection_end)
    


def _available(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    processed = editor.fEditor.GetCommandMap()._GetCommand('start_select_line')
    x = editor.CommandAvailable('start-select-line')
    with open(r'G:\Dropbox\Desktop\file.txt', mode='a') as log_file:
        log_file.write(str((x, processed, editor)))
    return True
    return x

#cute_start_select_line.available = (
    #_a
    ##lambda application:
                     ##wingapi.gApplication.CommandAvailable('start-select-line')
#)

