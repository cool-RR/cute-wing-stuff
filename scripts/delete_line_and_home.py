# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import wingapi

import shared


def delete_line_and_home():
    '''
    Delete the current line and send caret to beginning of text in next line.

    When you use Wing's default `delete-line` command to delete a line, it
    sends the caret to column 0, which is annoying. This script fixes that by
    first deleting a line, then sending the caret to the beginning of the text
    on the next line.

    Suggested key combination: `Ctrl-Shift-C`
    '''
    wingapi.gApplication.ExecuteCommand('delete-line')
    wingapi.gApplication.ExecuteCommand('beginning-of-line-text')

