# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import bisect
import re
import inspect
import logging

import wingapi

import shared

python_identifier_subpattern = r'''[a-zA-Z_][0-9a-zA-Z_]*'''

pattern = re.compile(
    r'''(?P<object>%s(?:\.%s)*)\.(?P<attribute_name>%s)''' % (
        python_identifier_subpattern, python_identifier_subpattern,
        python_identifier_subpattern
    )
)

def _get_matches(document):
    assert isinstance(document, wingapi.CAPIDocument)
    document_text = shared.get_text(document)
    return tuple(pattern.finditer(document_text))


def implicit_getattr_to_explicit():
    '''
    Convert something like `foo.bar` into `getattr(foo, 'bar', None)`.

    Also selects the `None` so it could be easily modified.

    Suggested key combination: `Insert Shift-G`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)


    _, current_position = shared.get_selection_unicode(editor)
    #head = max(current_position - 100, 0)
    #tail = min(current_position + 100, document.GetLength())

    #text = document.GetText()[head : tail]

    matches = _get_matches(document)
    if not matches:
        return
    match_spans = tuple(match.span(0) for match in matches)
    candidate_index = max(
        bisect.bisect_left(match_spans, (current_position, 0)) - 1,
        0
    )
    candidate_span = match_spans[candidate_index]
    candidate = matches[candidate_index]
    #if candidate[0] <= current_position <= candidate[1]:
        #shared.set_selection_unicode(editor, *candidate)
    #else:
        #print(candidate)
        #try:
            #print(shared.get_text(document)[candidate[0]:candidate[1]])
        #except:
            #pass

    new_text = 'getattr(%s, %s, None)' % (candidate.group(1),
                                          repr(candidate.group(2)))
    wingapi.gApplication.ExecuteCommand('set-visit-history-anchor')
    with shared.UndoableAction(document):
        document.DeleteChars(candidate_span[0], candidate_span[1] - 1)
        document.InsertChars(candidate_span[0], new_text)
        shared.set_selection_unicode(editor, candidate_span[0]+len(new_text)-5,
                            candidate_span[0]+len(new_text)-1)