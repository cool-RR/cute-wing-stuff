from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))


import wingapi

import shared

print(dir(_shared))


def arg_to_attr(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    with shared.UndoableAction(document):
        shared.select_current_word(editor)
        start, end = editor.GetSelection()
        variable_name = document.GetCharRange(start, end)
        result_string = 'self.%s = %s' % (variable_name, variable_name)
        document.DeleteChars(start, end)
        document.InsertChars(start, result_string)
        editor.SetSelection(start + len(result_string),
                            start + len(result_string))
        editor.ExecuteCommand('new-line')
    
        
