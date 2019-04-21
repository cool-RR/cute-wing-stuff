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

SMARTGITC_EXE_PATH = '"C:\\Program Files\\SmartGit\\bin\\smartgitc.exe"'


def launch_process_without_window(command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(' '.join(command), startupinfo=startupinfo)

def launch_smartgit(arguments):
    return launch_process_without_window([SMARTGITC_EXE_PATH] + arguments)
    

def smartgit(project=wingapi.kArgProject):
    '''
    Start SmartGit for the current project.
    
    Suggested key combination: `Insert G`    
    '''
    assert isinstance(project, wingapi.CAPIProject)
    launch_smartgit(['--open', project.ExpandEnvVars('"${WING:PROJECT_DIR}"')])
    
    
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
    launch_smartgit(['--blame', str('"%s:%s"' % (filename, line_number))])
    