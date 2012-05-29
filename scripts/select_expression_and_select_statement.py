# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `select_expression` and `select_statement` scripts.

See its documentation for more information.
'''

from __future__ import with_statement

import _ast

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


SAFETY_LIMIT = 40
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
    

def _is_statement(string):
    '''Is `string` a Python statement?'''
    
    string = '%s\n' % string
    # Throwing out '\r' characters because `ast` can't process them for some
    # reason:
    string = string.replace('\r', '')
    try:
        nodes = _ast_parse(string).body
    except SyntaxError:
        return False
    else:
        return len(nodes) == 1
    

def _select_more_until(condition, editor=wingapi.kArgEditor):
    '''`select-more` until the selected text satisfies `condition`.'''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    select_more = lambda: wingapi.gApplication.ExecuteCommand('select-more')
    is_selection_good = lambda: condition(
        document.GetCharRange(*editor.GetSelection()).strip()
    )

    last_expression_start = None
    last_expression_end = None
    
    last_start, last_end = editor.GetSelection()
    with shared.ScrollRestorer(editor):
        with shared.SelectionRestorer(editor):
            for i in range(SAFETY_LIMIT):
                select_more()
                current_start, current_end = editor.GetSelection()
                if (current_start == last_start) and (current_end == last_end):
                    break
                if is_selection_good():
                    last_expression_start, last_expression_end = \
                                                     current_start, current_end
                last_start, last_end = current_start, current_end
    
        assert (last_expression_start is None) == \
                                                (last_expression_start is None)
        if last_expression_start is not None:
            editor.SetSelection(last_expression_start, last_expression_end)
            shared.strip_selection_if_single_line(editor)
            
            
def select_expression(editor=wingapi.kArgEditor):
    '''
    Select the Python expression that the cursor is currently on.
    
    This does `select-more` until the biggest possible legal Python expression
    is selected.
    '''
    _select_more_until(_is_expression, editor)
            
            
def select_statement(editor=wingapi.kArgEditor):
    '''
    Select the Python statement that the cursor is currently on.
    
    This does `select-more` until the biggest possible legal Python statement
    is selected.
    '''
    _select_more_until(_is_statement, editor)
    
    
