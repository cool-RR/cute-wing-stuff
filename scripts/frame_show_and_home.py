# Copyright 2009-2012 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `frame_show_and_home` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def frame_show_and_home():
    '''
    Go to the line of the current frame and send caret to beginning of text.
    
    When you use Wing's default `frame-show` command to go to the line of the
    current frame, it sends the caret to column 0, which is annoying. This
    script fixes that by first doing `frame-show`, then sending the caret to
    the beginning of the text.
    '''
    wingapi.gApplication.ExecuteCommand('frame-show')
    wingapi.gApplication.ExecuteCommand('beginning-of-line-text')
    
    