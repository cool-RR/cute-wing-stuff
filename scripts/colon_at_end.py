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


def colon_at_end():
    '''
    Go to the end of the line and insert a colon.

    Suggested key combination: `Ctrl-Semicolon`
    '''
    app = wingapi.gApplication
    app.ExecuteCommand('end-of-line')
    app.ExecuteCommand('send-keys', keys=':')
