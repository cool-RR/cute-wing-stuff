# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `backward_half_page` script.

See its documentation for more information.
'''

from __future__ import division
from __future__ import with_statement

import time
import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared

    
def backward_half_page(editor=wingapi.kArgEditor):
    '''
    Move half a page up.
    
    This is essentially one half of Page-Up.
    '''
    shared._move_half_page(-1, editor=editor)
    