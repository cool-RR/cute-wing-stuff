# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines scripts for selecting stuff.

See their documentation for more information.
'''

from __future__ import with_statement

import bisect
import re
import _ast

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import wingapi

import shared


SAFETY_LIMIT = 60
'''The maximum number of times we'll do `select-more` before giving up.'''

def _ast_parse(string):
    return compile(string, '<unknown>', 'exec', _ast.PyCF_ONLY_AST)


def _is_expression(string):
    '''Is `string` a Python expression?'''

    # Throwing out '\r' characters because `ast` can't process them for some
    # reason:
    string = string.replace('\r', '')
    try:
        nodes = _ast_parse(string).body
    except SyntaxError:
        return False
    else:
        if len(nodes) != 1:
            return False
        else:
            (node,) = nodes
            return type(node) == _ast.Expr



variable_name_pattern_text = r'[a-zA-Z_][0-9a-zA-Z_]*'
dotted_name_pattern = re.compile(
    r'\.?^%s(\.%s)*$' %
                       (variable_name_pattern_text, variable_name_pattern_text)
)

def _is_dotted_name(string):
    '''Is `string` a dotted name?'''
    assert isinstance(string, str)
    return bool(dotted_name_pattern.match(string.strip()))


whitespace_characters = ' \n\r\t\f\v'

def _is_whitespaceless_name(string):
    '''Is `string` a whitespace-less name?'''
    assert isinstance(string, str)
    return not any((whitespace_character in string for whitespace_character
                in whitespace_characters))


def _select_more_until_biggest_match(condition):
    '''`select-more` until reaching biggest text that satisfies `condition`.'''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    select_more = lambda: wingapi.gApplication.ExecuteCommand('select-more')
    is_selection_good = lambda: condition(
        document.GetCharRange(*shared.get_selection_unicode(editor)).strip()
    )

    last_success_n_iterations = None

    last_start, last_end = original_selection = shared.get_selection_unicode(editor)

    with shared.ScrollRestorer(editor):
        with shared.SelectionRestorer(editor):
            for i in range(SAFETY_LIMIT):
                select_more()
                current_start, current_end = shared.get_selection_unicode(editor)
                if (current_start == last_start) and (current_end == last_end):
                    break
                if is_selection_good():
                    last_success_n_iterations = i
                last_start, last_end = current_start, current_end

        if last_success_n_iterations is not None:
            for i in range(last_success_n_iterations+1):
                select_more()


def select_expression():
    '''
    Select the Python expression that the cursor is currently on.

    This does `select-more` until the biggest possible legal Python expression
    is selected.

    Suggested key combination: `Ctrl-Alt-Plus`
    '''
    _select_more_until_biggest_match(_is_expression)


def select_dotted_name():
    '''
    Select the dotted name that the cursor is currently on, like `foo.bar.baz`.

    This does `select-more` until the biggest possible dotted name is selected.

    Suggested key combination: `Alt-Plus`
    '''
    _select_more_until_biggest_match(_is_dotted_name)


def select_whitespaceless_name():
    '''
    Select the whitespace-less name that the cursor is currently on.

    Example: `foo.bar.baz(e=3)`.

    This does `select-more` until the biggest possible whitespace-less name is
    selected.

    Suggested key combination: `Ctrl-Alt-Equal`
    '''
    _select_more_until_biggest_match(_is_whitespaceless_name)


_scope_name_pattern = re.compile(
    r'''(?:^|[ \t\r\n])(?:def|class) +([a-zA-Z_][0-9a-zA-Z_]*)'''
    r'''[ \t\r\n]*[(:]''',
    flags=re.DOTALL
)


def _get_scope_name_positions(document):
    document_text = shared.get_text(document)
    matches = _scope_name_pattern.finditer(document_text)
    return tuple(match.span(1) for match in matches)


def select_next_scope_name():
    '''
    Select the next scope name like `def thing():` or `class Thing():`.

    (Selects just the name.)

    Suggested key combination: `Alt-Semicolon`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    _, position = shared.get_selection_unicode(editor)
    position += 1

    scope_name_positions = _get_scope_name_positions(editor.GetDocument())
    scope_name_ends = tuple(scope_name_position[1] for scope_name_position in
                            scope_name_positions)
    scope_name_index = bisect.bisect_left(scope_name_ends, position)

    if 0 <= scope_name_index < len(scope_name_ends):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *scope_name_positions[scope_name_index])


def select_prev_scope_name():
    '''
    Select the previous scope name like `def thing():` or `class Thing():`.

    (Selects just the name.)

    Suggested key combination: `Alt-Colon`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    app = wingapi.gApplication
    position, _ = shared.get_selection_unicode(editor)
    position -= 1

    scope_name_positions = _get_scope_name_positions(editor.GetDocument())
    scope_name_starts = tuple(scope_name_position[0] for scope_name_position
                              in scope_name_positions)
    scope_name_index = bisect.bisect_left(scope_name_starts, position) - 1

    if 0 <= scope_name_index < len(scope_name_starts):
        app.ExecuteCommand('set-visit-history-anchor')
        shared.set_selection_unicode(editor, *scope_name_positions[scope_name_index])

