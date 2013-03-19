# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `run_command_and_clip_ahk` script.

See its documentation for more information.
'''


from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import re
import inspect

import wingapi

import shared



def run_command_and_clip_ahk(command):
    '''
    Experimental.
    '''
    application = wingapi.gApplication
    assert isinstance(command, basestring)
    assert isinstance(application, wingapi.CAPIApplication)
    application.ExecuteCommand(command)
    if shared.autopy_available:
        shared.clip_ahk()