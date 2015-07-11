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

import shared


def run_command_idempotent(command_name, application=wingapi.kArgApplication):
    '''Run a command, first terminating any running instances of it.'''
    assert isinstance(application, wingapi.CAPIApplication)
    panel = application.fSingletons.fGuiMgr.ShowPanel(config.kOSCommandPanel)
    if not panel:
        return
    command = panel._FindCmdByTitle(command_name)
    application.TerminateOSCommand(command.id)
    application.ExecuteOSCommand(command.id)
        
        
        