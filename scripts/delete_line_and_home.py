# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `delete_line_and_home` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def delete_line_and_home():
    '''
    Delete the current line and send caret to beginning of text in next line.
    
    When you use Wing's default `delete-line` command to delete a line, it
    sends the caret to column 0, which is annoying. This script fixes that by
    first deleting a line, then sending the caret to the beginning of the text
    on the next line.
    '''
    wingapi.gApplication.ExecuteCommand('delete-line')
    wingapi.gApplication.ExecuteCommand('beginning-of-line-text')
    
    