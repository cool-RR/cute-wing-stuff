# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import wingapi

import shared


toggle_state = False


def debug_toggle_value_tips():
    '''
    Show or hide value tips while debugging. 

    Suggested key combination: `Shift-space`
    '''
    global toggle_state
    if toggle_state:
        wingapi.gApplication.ExecuteCommand('debug_hide_value_tips')
    else:
        wingapi.gApplication.ExecuteCommand('debug_show_value_tips')
    toggle_state = not toggle_state
        


debug_toggle_value_tips.available = (
    lambda editor=wingapi.kArgEditor:
                 wingapi.gApplication.CommandAvailable('debug_show_value_tips')
)
