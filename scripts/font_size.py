# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import wingapi


def font_big():
    '''Set the editor font size to 9 points.'''
    application = wingapi.gApplication
    assert isinstance(application, wingapi.CAPIApplication)
    application.SetPreference('edit.qt-display-font', 'Consolas,9')


def font_small():
    '''Set the editor font size to 8 points.'''
    application = wingapi.gApplication
    assert isinstance(application, wingapi.CAPIApplication)
    application.SetPreference('edit.qt-display-font', 'Consolas,8')