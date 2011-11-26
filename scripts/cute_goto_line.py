# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `cute_goto_line` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi
import wingutils.datatype
import guiutils.formbuilder 
 
import shared


def cute_goto_line():
    '''blocktododoc'''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    
    line_number = 7    
    line_number = int(line_number)
    original_show_line_numbers_setting = \
                   wingapi.gApplication.GetPreference('edit.show-line-numbers')
    #try:
    wingapi.gApplication.SetPreference('edit.show-line-numbers', True)
    editor.ExecuteCommand('goto-line', gotoline=7)
    #finally:
    wingapi.gApplication.SetPreference('edit.show-line-numbers',
                                       original_show_line_numbers_setting)
    
        
#cute_goto_line.arginfo = {
    #'line_number': wingapi.CArgInfo('Line number',
                                    #wingutils.datatype.CType(1),
                                    #guiutils.formbuilder.CNumberGui(
                                        #0,
                                        #1000000,
                                        #5,
                                        #0
                                    #),
                                    #'Line number',),
#}