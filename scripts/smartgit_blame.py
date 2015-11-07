# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import inspect
import subprocess

import wingapi
import config

import shared

SMARTGITC_EXE_PATH = '"C:\\Program Files (x86)\\SmartGit\\bin\\smartgitc.exe"'


def smartgit_blame(editor=wingapi.kArgEditor):
    '''
    Start SmartGit blame on the currently selected line.
    
    Suggested key combination: `Insert Ctrl-B`    
    '''
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    filename = document.GetFilename()
    line_number = document.GetLineNumberFromPosition(editor.GetSelection()[0])
    shell_command = ' '.join([
        SMARTGITC_EXE_PATH, '--blame',
        '"%s":%s' % (filename, line_number)
    ])
    popen = subprocess.Popen(shell_command)
    