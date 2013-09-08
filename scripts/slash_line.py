# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `slash_line` script.

See its documentation for more information.
'''


from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import wingapi

import shared


def slash_line(editor=wingapi.kArgEditor, line_offset=0, at_caret=False):
    '''
    Slash a long line into 2 lines, putting a `\` character as a separator.
    
    This is good for automatically formatting long lines into this style:

        has_corresponding_source_file = \
                               os.path.exists(corresponding_python_source_file)
        nose.selector.Selector.wantFile = \
                       types.MethodType(wantFile, None, nose.selector.Selector)
                       
    Specify `line_offset` to slash a line different from the one that the caret
    is on. For example, `line_offset=-1` would slash the previous line.
    
    Specify `at_caret=True` to use the current caret position as the slashing
    point, rather than finding one automatically.

    Suggested key combination: `Insert L` for default arguments,
    `Insert Shift-L` for line_offset=-1, and `Insert Ctrl-L` for
    at_caret=True.
    '''
    
    if at_caret:
        assert not line_offset
        caret_position, _ = editor.GetSelection()
        

    max_line_length = \
        wingapi.gApplication.GetPreference('edit.text-wrap-column')
    
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    position, _ = editor.GetSelection()
    line = document.GetLineNumberFromPosition(position) + line_offset
    line_start = document.GetLineStart(line)
    line_end = document.GetLineEnd(line)
    line_content = document.GetCharRange(line_start, line_end)
    current_line_length = line_end - line_start
    
    if current_line_length <= max_line_length:
        return 
    
    assert current_line_length > max_line_length
    
    ### Determining where to put the slash: ###################################
    #                                                                         #
    content_segment = line_content[:max_line_length-1]
    if at_caret:
        caret_position_in_line = caret_position - line_start
        slash_position = content_segment.find(' ',
                                              caret_position_in_line - 1) + 1
    else:
        if ' = ' in content_segment:
            slash_position = content_segment.find(' = ') + 3
        else:
            slash_position = content_segment.rfind(' ') + 1
    #                                                                         #
    ### Finished determining where to put the slash. ##########################
    
    absolute_slash_position = slash_position + line_start
    
    with shared.UndoableAction(document):
        with shared.SelectionRestorer(editor, line_wise=True, line_offset=1):
            document.InsertChars(absolute_slash_position, '\\')
            editor.SetSelection(absolute_slash_position + 1,
                                absolute_slash_position + 1)
            editor.ExecuteCommand('new-line')
            wingapi.gApplication.ExecuteCommand('push-line-to-end')