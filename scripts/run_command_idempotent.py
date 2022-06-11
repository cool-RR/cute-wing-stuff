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


def run_command_idempotent(command_name):
    '''Run a command, first terminating any running instances of it.'''
    app = wingapi.gApplication
    assert isinstance(app, wingapi.CAPIApplication)
    panel = app.fSingletons.fGuiMgr.ShowPanel(config.kOSCommandPanel)
    if not panel:
        return
    command = panel._FindCmdByTitle(command_name)
    app.TerminateOSCommand(command.id)
    app.ExecuteOSCommand(command.id)


