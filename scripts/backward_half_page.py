# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `backward_half_page` script.

See its documentation for more information.
'''

from __future__ import division
from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared

    
def backward_half_page(editor=wingapi.kArgEditor):
    '''
    Move half a page up.
    
    This is essentially one half of Page-Up.
    
    Suggested key combination: `Alt-Page_up` (As long as you don't use Wing's
    folding.)
    '''
    shared.reset_caret_blinking(editor)
    shared._move_half_page(-1, editor=editor)
    