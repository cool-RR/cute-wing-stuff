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

flip_pairs = (
    ('True', 'False'),
    ('true', 'false'),
    ('enable', 'disable'),
    ('add', 'remove'),
    ('start', 'end'),
    ('head', 'tail'),
    ('low', 'high'),
    ('first', 'last'),
    ('import', 'export'),
    ('left', 'right'),
    ('early', 'late'),
    ('earliest', 'latest'),
    ('new', 'old'),
    ('maximum', 'minimum'),
    ('max', 'min'),
    ('next', 'previous'),
    ('width', 'height'),
    ('column', 'row'),
    ('horizontal', 'vertical'),
    ('horizontally', 'vertically'),
    ('on', 'off'),
    ('before', 'after'),
    ('opening', 'closing'),
    ('read', 'write'),
    ('reader', 'writer'),
    ('reading', 'writing'),
    ('readable', 'writable'),
    ('private', 'public'),
    ('encode', 'decode'),
    ('encoding', 'decoding'),
    ('request', 'response'),
    ('big', 'small'),
    ('color', 'grayscale'),
    ('get', 'set'),
    ('accept', 'reject'),
    ('enter', 'exit'),
    ('up', 'down'),
    ('visible', 'hidden'),
    ('above', 'below'),
    ('pre', 'post'),
)

all_words = sum(flip_pairs, ())


def _is_any_word_on_caret(document_text, caret_position, words):
    ''' '''
    sorted_words = sorted(words, key=len, reverse=True)
    max_word_length = len(sorted_words[0])
    first_cut_point = max(caret_position - max_word_length, 0)
    second_cut_point = min(caret_position + max_word_length,
                           len(document_text))
    cut_text = document_text[first_cut_point:second_cut_point]
    caret_position_in_cut_text = caret_position - first_cut_point
    words_in_cut_text = [word for word in sorted_words if word in cut_text]
    for word in words_in_cut_text:
        word_start_position_in_cut_text = cut_text.find(word)
        word_end_position_in_cut_text = cut_text.find(word) + len(word)
        if word_start_position_in_cut_text <= caret_position_in_cut_text <= \
                                                 word_end_position_in_cut_text:
            word_start_position = word_start_position_in_cut_text + \
                                                                first_cut_point
            return (word, word_start_position)
    else:
        return (None, None)

def flip():
    '''
    Flip between opposite words.

    Put the caret on a word like `True` or `start` or `new` and watch it change
    into `False` or `end` or `old`.

    Suggested key combination: `Insert P`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)

    with shared.UndoableAction(document):
        word, word_start_position = _is_any_word_on_caret(
            shared.get_text(document),
            shared.get_selection_unicode(editor)[0],
            all_words
        )
        if not word:
            return

        for first_word, second_word in flip_pairs:
            if first_word == word:
                new_word = second_word
                break
            elif second_word == word:
                new_word = first_word
                break
            else:
                continue
        else:
            raise RuntimeError

        with shared.SelectionRestorer(editor):
            document.DeleteChars(word_start_position,
                                 word_start_position + len(word) - 1)
            document.InsertChars(word_start_position, new_word)


