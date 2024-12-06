# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]

import os
import subprocess
import wingapi
import tempfile

def almost_edit_in_cursor_ide():
    '''
    Almost open the current file in Cursor IDE.

    Saves the file, copies its path to clipboard and changes focus to the Cursor IDE.

    Suggested key combination: `Ctrl-Bar` (`Ctrl-Shift-\`)
    '''
    if sys.platform != 'win32':
        wingapi.gApplication.ShowMessageDialog('Error',
                                               'This command only works on Windows.')
        return

    editor = wingapi.gApplication.GetActiveEditor()
    if not editor:
        return

    doc = editor.GetDocument()
    doc.Save()

    wingapi.gApplication.ExecuteCommand('copy-file-path')
    ahk_script = "WinActivate ahk_exe Cursor.exe\nExitApp"
    with tempfile.NamedTemporaryFile(suffix='.ahk', mode='w', delete=False) as f:
        f.write(ahk_script)
        temp_script_path = f.name

    try:
        subprocess.run([r'C:\Program Files\AutoHotkey\AutoHotkey.exe', temp_script_path])
    finally:
        os.unlink(temp_script_path)
