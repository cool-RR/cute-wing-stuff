# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import sys
import inspect

import wingapi

import shared

TAB_KEY = 15 if 'linux' in sys.platform else '48' if 'darwin' in sys.platform \
                                                                         else 9


_characters_that_need_shift = ('!@#$%^&*()_+~{}>:"?|<')

def _type_string(string):
    assert shared.autopy_available
    import autopy.key
    for character in string:
        if character in _characters_that_need_shift:
            autopy.key.tap(character, [autopy.key.Modifier.SHIFT])
        else:
            autopy.key.tap(character, [])
        shared.clip_ahk()
        autopy.key.tap(autopy.key.Code.END, []) # `End` for making AHK not interfere


def _cute_general_replace(command_name, editor):
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    assert isinstance(app, wingapi.CAPIApplication)
    selection_start, selection_end = editor.GetSelection()
    selection = editor.GetDocument().GetCharRange(selection_start,
                                                  selection_end)

    if selection:
        wingapi.gApplication.SetClipboard(selection)
        editor.SetSelection(selection_start, selection_start)
        app.ExecuteCommand(command_name)
        # if shared.autopy_available:
            # import autopy.key
            # autopy.key.toggle(autopy.key.Modifier.ALT, False, [])
            # autopy.key.toggle(autopy.key.Modifier.SHIFT, False, [])
            # autopy.key.toggle(autopy.key.Modifier.CONTROL, False, [])
            # autopy.key.toggle(autopy.key.Modifier.META, False, [])
            #_type_string(selection)
            #autopy.key.tap(autopy.key.Code.ESC)
            #autopy.key.toggle(autopy.key.Modifier.ALT, False)
            #autopy.key.tap(TAB_KEY)
            #autopy.key.tap('l', autopy.key.Modifier.ALT)
            #autopy.key.tap('v', autopy.key.Modifier.CONTROL)
            #autopy.key.tap('a', autopy.key.Modifier.CONTROL)


    else: # not selection
        app.ExecuteCommand(command_name)


def cute_query_replace():
    '''
    Improved version of `query-replace` for finding and replacing in document.

    BUGGY: If text is selected, it will be used as the text to search for, and
    the contents of the clipboard will be offered as the replace value.

    Implemented on Windows only.

    Suggested key combination: `Alt-Comma`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    return _cute_general_replace('query-replace', editor=editor)


def cute_replace_string():
    '''
    Improved version of `replace-string` for finding and replacing in document.

    BUGGY: If text is selected, it will be used as the text to search for, and
    the contents of the clipboard will be offered as the replace value.

    Implemented on Windows only.

    Suggested key combination: `Alt-Period`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    return _cute_general_replace('replace-string', editor=editor)