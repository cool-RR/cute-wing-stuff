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


def comma_newline_at_end():
    '''
    Go to the end of the line, insert a comma and a newline.

    Suggested key combination: `Ctrl-Comma`
    '''
    app = wingapi.gApplication
    editor = app.GetActiveEditor()
    app.ExecuteCommand('end-of-line')
    app.ExecuteCommand('send-keys', keys=',')
    editor.ExecuteCommand('new-line')
