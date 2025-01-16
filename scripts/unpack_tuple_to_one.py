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


def unpack_tuple_to_one():
    '''
    Turn `things` into `(thing,)`.

    Useful for writing things like:

        (thing,) == things

    See this blog post for more context: http://blog.ram.rachum.com/post/1198230058/python-idiom-for-taking-the-single-item-from-a-list

    Suggested key combination: `Insert U`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()

    assert isinstance(document, wingapi.CAPIDocument)

    with shared.UndoableAction(document):
        start, end = shared.select_current_word(editor)
        plural_word = document.GetText()[start : end]
        if not plural_word.endswith('s'):
            return
        singular_word = shared.plural_word_to_singular_word(plural_word)

        segment_to_insert = '(%s,)' % singular_word
        document.DeleteChars(start, end - 1)
        document.InsertChars(start, segment_to_insert)

        new_position = start + len(segment_to_insert)
        shared.set_selection_unicode(editor, new_position, new_position)