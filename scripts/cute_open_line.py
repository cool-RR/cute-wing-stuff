# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `cute_open_line` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def cute_open_line(editor=wingapi.kArgEditor):
    '''
    Open a new line, but don't move the caret down to the new line.
    
    Running this command is like pressing Enter, except your caret doesn't move
    into the new line that was created, but stays exactly where it was.
    
    The advantage of this over Wing's built-in `open-line` is that
    `cute-open-line` doesn't just insert a newline character like `open-line`
    does; it runs Wing's `new-line` command, which does various intelligent
    things like auto-indenting your code to the right level, opening your
    parentheses *just so* if you're doing function invocation, and a bunch of
    other goodies.
    '''
    
    assert isinstance(editor, wingapi.CAPIEditor)
    with shared.SelectionRestorer(editor):
        wingapi.gApplication.ExecuteCommand('new-line')
    
