# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import inspect
import subprocess
import os

import wingapi
import config

import shared

SMARTGITC_EXE_PATH = '"C:\\Program Files\\SmartGit\\bin\\smartgitc.exe"'


def launch_process_without_window(command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen(' '.join(command), startupinfo=startupinfo)

def launch_smartgit(arguments):
    return launch_process_without_window([SMARTGITC_EXE_PATH] + arguments)

def find_git_root(start_path):
    '''
    Walk up the directory tree from start_path to find a .git folder.
    Returns the git root directory path as a string, or None if not found.
    '''
    # Use os.path instead of pathlib to avoid Wing's monkey-patching issues
    current = os.path.abspath(start_path)

    # Walk up the directory tree
    while True:
        git_dir = os.path.join(current, '.git')

        if os.path.exists(git_dir) and os.path.isdir(git_dir):
            return current

        parent = os.path.dirname(current)
        if parent == current:
            # Reached the root
            break
        current = parent

    return None


def smartgit():
    '''
    Start SmartGit for the project's git repository root.
    Tries main entry point first, then searches project files.

    Suggested key combination: `Insert G`
    '''
    app = wingapi.gApplication
    project = app.GetProject()
    assert isinstance(project, wingapi.CAPIProject)

    git_root = None

    # Try main entry point first
    main_entry_point = project.GetMainEntryPoint()
    if main_entry_point and not main_entry_point.startswith('entry:'):
        # It's a file path, not a named entry point
        git_root = find_git_root(os.path.dirname(main_entry_point))

    # Fall back to first project file alphabetically
    if git_root is None:
        all_files = project.GetAllFiles()
        # Sort and get first non-remote file
        local_files = [f for f in sorted(all_files) if not f.startswith('ssh:')]
        if local_files:
            git_root = find_git_root(os.path.dirname(local_files[0]))

    if git_root is None:
        app.ShowMessageDialog(
            'Git Repository Not Found',
            'No .git folder found in main entry point or any project files.'
        )
        return

    launch_smartgit(['--open', f'"{git_root}"'])


def smartgit_blame():
    '''
    Start SmartGit blame on the currently selected line.

    Suggested key combination: `Insert Ctrl-B`
    '''
    editor = wingapi.gApplication.GetActiveEditor()
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    filename = document.GetFilename()
    line_number = document.GetLineNumberFromPosition(shared.get_selection_unicode(editor)[0])
    launch_smartgit(['--blame', str('"%s:%s"' % (filename, line_number))])
