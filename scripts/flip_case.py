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


def flip_case():
    '''
    Flip the case of the current word between undercase and camelcase.

    For example, if the cursor is on `something_like_this` and you activate
    this script, you'll get `SomethingLikeThis`. Do it again and you'll get
    `something_like_this` again.

    Suggested key combination: `Insert C`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    with shared.UndoableAction(document):
        start, end = shared.select_current_word(editor)
        word = document.GetCharRange(start, end)

        is_lower_case = word.islower()
        is_camel_case = not is_lower_case

        if is_lower_case:
            new_word = shared.lower_case_to_camel_case(word)

        else:
            assert is_camel_case
            new_word = shared.camel_case_to_lower_case(word)

        document.DeleteChars(start, end-1)
        document.InsertChars(start, new_word)
        shared.set_selection_unicode(editor, start + len(new_word),
                            start + len(new_word))
        #editor.ExecuteCommand('new-line')


