# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import division
from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import wingapi

import shared


def backward_half_page():
    '''
    Move half a page up.

    This is essentially one half of Page-Up.

    Suggested key combination: `Alt-Page_up` (As long as you don't use Wing's
    folding.)
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    shared.reset_caret_blinking(editor)
    shared._move_half_page(-1, editor=editor)
