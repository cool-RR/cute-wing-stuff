# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import sys
import subprocess

import wingapi
import pyperclip

def copy_file_path():
    '''
    Copy the full path of the current file to the clipboard.

    Suggested key combination: `Ctrl-Start-F`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    if editor is None:
        return

    file_path = editor.GetDocument().GetFilename()
    if sys.platform == 'win32':
        file_path = subprocess.list2cmdline([file_path])

    pyperclip.copy(file_path)
