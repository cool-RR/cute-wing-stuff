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


def cute_goto_line(editor=wingapi.kArgEditor):
    '''
    Go to a specified line number in editor, temporarily showing line numbers.
    
    This script is intended for people who don't like Wing to always show line
    numbers in the editors, but who *do* want to see them temporarily when
    using Wing's `goto-line` command, usually invoked by Ctrl-L, to go to a
    specific line.
    
    Using this script you can see exactly which line you're going to before
    issuing the command; and if usually keep line numbers hidden, then they
    will be hidden automatically after Wing has moved to the specified line.
    
    Also, the caret will go to the beginning of the text on the line instead of
    Wing's default of going to column 0.

    Suggested key combination: `Ctrl-L`
    '''
    assert isinstance(editor, wingapi.CAPIEditor)

    original_show_line_numbers_setting = \
                   wingapi.gApplication.GetPreference('edit.show-line-numbers')
    wingapi.gApplication.SetPreference('edit.show-line-numbers', True)
    
    def hide_if_was_hidden(*args, **kwargs):
        '''Restore the `show-line-numbers` setting to its original value.'''
        wingapi.gApplication.SetPreference(
            'edit.show-line-numbers',
            original_show_line_numbers_setting
        )
        wingapi.gApplication.ExecuteCommand('beginning-of-line-text')
        editor.disconnect(binding_tag)
        
    wingapi.gApplication.ExecuteCommand('goto-line')
    binding_tag = editor.connect('selection-changed', hide_if_was_hidden)
    
    
