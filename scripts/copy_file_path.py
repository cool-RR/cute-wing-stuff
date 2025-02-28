# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import sys
import os
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]
import subprocess
import pathlib

import wingapi
import pyperclip

import shared


def posh_if_available(path_string: str) -> str:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    posh_path = pathlib.Path(os.environ.get('DX', '')) / 'bin' / 'Common' / 'posh'
    try:
        result = subprocess.run([shared.python_executable, str(posh_path), path_string],
                                startupinfo=startupinfo, capture_output=True, text=True,
                                encoding='utf-8')
    except FileNotFoundError:
        pass
    if result.returncode == 0:
        return result.stdout.strip()
    return path_string


def copy_file_path() -> None:
    '''
    Copy the full path of the current file to the clipboard.

    Suggested key combination: `Ctrl-Start-F`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    if editor is None:
        return

    path_string = editor.GetDocument().GetFilename()
    if sys.platform == 'win32':
        path_string = subprocess.list2cmdline([path_string])
    path_string = posh_if_available(path_string)

    pyperclip.copy(path_string)
