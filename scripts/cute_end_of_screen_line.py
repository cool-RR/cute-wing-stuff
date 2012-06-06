# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def cute_end_of_screen_line(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    caret_position = editor.fEditor._fScint.get_current_pos()
    #editor.fEditor._fScint.line_end_display()
    #def help(func):
        #import inspect
        #return inspect.getargspec(func)
    
    
    print(editor.fEditor._fScint.get_position_cache())

    
    
    
    
