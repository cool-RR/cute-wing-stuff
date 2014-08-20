# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from  __future__ import with_statement

import wingapi


def wrap_lines_toggle():
    '''Toggle whether Wing wraps lines or not.'''
    application = wingapi.gApplication
    assert isinstance(application, wingapi.CAPIApplication)
    application.SetPreference('edit.wrap-lines',
                              not application.GetPreference('edit.wrap-lines'))