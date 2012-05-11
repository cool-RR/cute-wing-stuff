# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `go_to_lowest_project_frame` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def _normalize_path(path):
    ''' '''
    if not sys.platform.startswith('win'):
        return os.path.realpath(path)
    else:
        return os.path.realpath(path).lower()


def go_to_lowest_project_frame(application=wingapi.gApplication):
    '''
    Go to the lowest frame that's on project file rather than external module.

    Did you ever have Wing stop on an exception, and then drop you in code that
    belongs to an external module? This is often annoying, because you want to
    figure out what you did wrong on *your* code, and the external module is
    usually not to blame.
    
    `go-to-lowest-project-frame` to the rescue! Invoke this script while
    debugging in order to be taken to the lowest stack frame that's on a
    project file rather than an external module.
    '''
    project = application.GetProject()
    debugger = application.GetDebugger()
    all_project_files = set(map(_normalize_path, project.GetAllFiles()))
    _current_run_state = debugger.GetCurrentRunState()
    _thread_id, _frame_index = _current_run_state.GetStackFrame()
    _stack = _current_run_state.GetStack()
    
    if not _stack:
        return 
    
    file_paths = [_normalize_path(file_path) for file_path, _, _, _, _ in
                  _stack]
    
    file_paths_in_project = filter(
        lambda (_, file_path): file_path in all_project_files,
        enumerate(file_paths)
    )
    if not file_paths_in_project:
        return 
    index_of_last_file_path_in_project = file_paths_in_project[-1][0]
    
    _current_run_state.SetStackFrame(_thread_id,
                                     index_of_last_file_path_in_project)


def _available(application=wingapi.gApplication):
    ''' '''
    return bool(
        wingapi.gApplication.GetDebugger().GetCurrentRunState().GetStack()
    )

go_to_lowest_project_frame.available = _available

