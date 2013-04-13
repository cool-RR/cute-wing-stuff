# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines scripts for selecting stuff.

See its documentation for more information.
'''

from __future__ import with_statement

import re
import _ast

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def cute_new_line_before(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    with shared.UndoableAction(editor, enhanced=True):
        editor.ExecuteCommand('new-line-before')
    