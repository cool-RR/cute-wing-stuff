# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import _ast

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import wingapi

import shared


def brace_match_inner():
    '''
    Select the inside of the current/next pair of braces.

    Similar to Wing's built-in `brace-match`, except it selects only the inside
    of the braces, not including the braces themselves.

    Known limitations: Misses some pairs of braces. Doesn't know to ignore
    braces found in strings.

    Suggested key combination: `Alt-Bracketright`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    shared.set_selection_unicode(editor, shared.get_selection_unicode(editor)[0]-1, shared.get_selection_unicode(editor)[1]+1)
    editor.ExecuteCommand('brace-match')
    shared.set_selection_unicode(editor, shared.get_selection_unicode(editor)[0]+1, shared.get_selection_unicode(editor)[1]-1)


def previous_brace_match():
    '''
    Select the previous pair of braces.

    Similar to Wing's built-in `brace-match`, except it goes backwards instead
    of going forwards. Goes to the nearest pair of braces, whether it's (), [],
    or {} that's before the current caret position, and selects those braces
    including all their content.

    Known limitations: Misses some pairs of braces. Doesn't know to ignore
    braces found in strings.

    Suggested key combination: `Ctrl-Bracketleft`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    document_text = shared.get_text(document)
    _, caret_position = shared.get_selection_unicode(editor)
    closing_brace_position = max((
        document_text.rfind(')', 0, caret_position - 1),
        document_text.rfind(']', 0, caret_position - 1),
        document_text.rfind('}', 0, caret_position - 1)
    ))
    if closing_brace_position == -1:
        return
    new_position = closing_brace_position
    shared.set_selection_unicode(editor, new_position, new_position)
    editor.ExecuteCommand('brace-match')


def previous_brace_match_inner():
    '''
    Select the inside of the previous pair of braces.

    Similar to Wing's built-in `brace-match`, except it goes backwards instead
    of going forwards. Goes to the nearest pair of braces, whether it's (), [],
    or {} that's before the current caret position, and selects the content of
    those braces, not including the braces themselves.

    Known limitations: Misses some pairs of braces. Doesn't know to ignore
    braces found in strings.

    Suggested key combination: `Alt-Bracketleft`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    shared.set_selection_unicode(editor, shared.get_selection_unicode(editor)[0]+1, shared.get_selection_unicode(editor)[1]-1)
    previous_brace_match()
    shared.set_selection_unicode(editor, shared.get_selection_unicode(editor)[0]+1, shared.get_selection_unicode(editor)[1]-1)