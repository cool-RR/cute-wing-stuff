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


def smartgit(project=wingapi.kArgProject):
    '''
    Start SmartGit for the current project.
    
    Suggested key combination: `Insert G`    
    '''
    assert isinstance(project, wingapi.CAPIProject)
    shell_command = ' '.join([
        SMARTGITC_EXE_PATH, '--open',
        project.ExpandEnvVars('"${WING:PROJECT_DIR}"')
    ])
    popen = subprocess.Popen(shell_command)
    