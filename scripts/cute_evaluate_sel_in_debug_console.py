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


def cute_evaluate_sel_in_debug_console():
    '''
    Evaluate selection in debug console, do `select-more` if no selection.

    Suggested key combination: `Ctrl-Alt-D`
    '''

    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    selection_start, selection_end = shared.get_selection_unicode(editor)
    if selection_start == selection_end:
        editor.ExecuteCommand('select-more')

    wingapi.gApplication.ExecuteCommand('evaluate-sel-in-debug-console')