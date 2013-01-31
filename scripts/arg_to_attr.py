# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `arg_to_attr` script.

See its documentation for more information.
'''


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import inspect

import wingapi

import shared


def arg_to_attr(editor=wingapi.kArgEditor):
    '''
    Turn an argument to `__init__` into an instance attribute.
    
    For example, you have just typed this:
    
        class MyObject(object):
            def __init__(self, crunchiness):
                <Cursor is here>
                
    (Of course, you can substitute `crunchiness` for whatever your argument's
    name is.)
    
    Now, you might want to put a `self.crunchiness = crunchiness` line in that
    `__init__` method. But that would take so much typing, because
    `self.crunchiness` doesn't exist yet, and won't be autocompleted. That
    would require you to make around 20 keystrokes. I don't know about you, but
    I'm just not ready for that kind of a commitment.
    
    Instead, type `crunchiness`. (You'll get autocompletion because it exists
    as an argument.) Then run this `arg_to_attr` script. (I personally use
    `Insert A` for it.)
    
    The final result is that you'll get a `self.crunchiness = crunchiness` line
    and have the cursor ready in the next line.
    
    Suggested key combination: `Insert A`    
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    with shared.UndoableAction(document):
        start, end = shared.select_current_word(editor)    
        variable_name = document.GetCharRange(start, end)
        result_string = 'self.%s = %s' % (variable_name, variable_name)
        document.DeleteChars(start, end - 1)
        document.InsertChars(start, result_string)
        editor.SetSelection(start + len(result_string),
                            start + len(result_string))
        editor.ExecuteCommand('new-line')
    
        
