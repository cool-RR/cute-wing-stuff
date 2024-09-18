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


def show_file_in_explorer():
    '''
    Show currently-open file in explorer.

    Suggested key combination: `Insert Comma`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    shared.show_file_in_explorer(editor.GetDocument().GetFilename())
