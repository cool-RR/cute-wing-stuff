# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `show_file_in_explorer` script.

See its documentation for more information.
'''

from __future__ import division
from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared

    
def show_file_in_explorer(editor=wingapi.kArgEditor):
    '''
    Open the currently-edited file's folder in Explorer.
    
    Implementd only for Windows.
    '''
    # todo feature: Select the file in the Explorer window after opening it.
    assert isinstance(editor, wingapi.CAPIEditor)
    if os.name != 'nt':
        raise NotImplemented('Implemented for Windows only, sorry!')
    path_to_file = editor.GetDocument().GetFilename()
    folder, _ = os.path.split(path_to_file)
    os.startfile(folder)