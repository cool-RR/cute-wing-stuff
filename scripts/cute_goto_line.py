# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `cute_goto_line` script.

See its documentation for more information.
'''

from __future__ import with_statement

import threading
import time
import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi
import wingutils.datatype
import guiutils.formbuilder 
 
import shared


def cute_goto_line():
    '''blocktododoc'''

    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    #document = editor.GetDocument()
    #assert isinstance(document, wingapi.CAPIDocument)

    original_show_line_numbers_setting = \
                   wingapi.gApplication.GetPreference('edit.show-line-numbers')
    wingapi.gApplication.SetPreference('edit.show-line-numbers', True)
    
    def hide_if_was_hidden():
        ''' '''
        wingapi.gApplication.SetPreference(
            'edit.show-line-numbers',
            original_show_line_numbers_setting
        )
        
    wingapi.gApplication.ExecuteCommand('goto-line')
    wingapi.gApplication.InstallTimeout(3000, hide_if_was_hidden)
    #editor.connect('selection-changed', hide_if_was_hidden)
