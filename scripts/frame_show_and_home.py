# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `frame_show_and_home` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]


import wingapi

import shared


def frame_show_and_home():
    '''
    Go to the line of the current frame and send caret to beginning of text.
    
    When you use Wing's default `frame-show` command to go to the line of the
    current frame, it sends the caret to column 0, which is annoying. This
    script fixes that by first doing `frame-show`, then sending the caret to
    the beginning of the text.

    Suggested key combination: `Shift-F11`
    '''
    wingapi.gApplication.ExecuteCommand('frame-show')
    wingapi.gApplication.ExecuteCommand('beginning-of-line-text')
    
    