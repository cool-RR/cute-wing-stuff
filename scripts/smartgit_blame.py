# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import inspect

import wingapi
import config
# import sarge

import shared


def smartgit_blame(command_name, editor=wingapi.kArgEditor):
    '''Start SmartGit blame on the currently selected line.'''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    filename = document.GetFilename()
    # line_number = document.GetLineNumberFromPosition(editor.GetSelection()[0])
    # sarge.run(
        # ['"C:\\Program Files (x86)\\SmartGit\\bin\\smartgitc.exe"', '--blame',
         # '"%s:"' % (filename, line_number)],
        # async=True
    # )
    # print(' '.join(
        # ['"C:\\Program Files (x86)\\SmartGit\\bin\\smartgitc.exe"', '--blame',
         # '"%s:"' % (filename, line_number)]))