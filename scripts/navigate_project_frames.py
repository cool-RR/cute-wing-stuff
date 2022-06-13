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


def _normalize_path(path):
    ''' '''
    if not sys.platform.startswith('win'):
        return os.path.realpath(path)
    else:
        return os.path.realpath(path).lower()


def go_up_to_project_frame(application=wingapi.gApplication):
    '''
    Go up one frame in the debugger, skipping any non-project frames.

    Did you ever have Wing stop on an exception, and then drop you in code that
    belongs to an external module? This is often annoying, because you want to
    figure out what you did wrong on *your* code, and the external module is
    usually not to blame.

    `go-up-to-project-frame` to the rescue! Invoke this script while debugging
    in order to be taken to the closest higher stack frame that's on a project
    file rather than an external module.

    Suggested key combination: `Alt-F11`
    '''
    project = application.GetProject()
    debugger = application.GetDebugger()
    all_project_files = set(map(_normalize_path, project.GetAllFiles()))
    _current_run_state = debugger.GetCurrentRunState()
    _thread_id, (_, _frame_index) = _current_run_state.GetStackIndex()
    _stack = _current_run_state.GetStack()
    if not _stack:
        return

    file_paths = [_normalize_path(file_path) for file_path, _, _, _, _ in
                  _stack]
    file_paths_in_project_above_current_frame = tuple(
        filter(
            lambda i_and_file_path: i_and_file_path[1] in all_project_files and
                                                                  i_and_file_path[0] < _frame_index,
            enumerate(file_paths)
        )
    )
    if not file_paths_in_project_above_current_frame:
        return
    index_of_last_file_path_in_project = \
                               file_paths_in_project_above_current_frame[-1][0]

    _current_run_state.SetStackIndex(_thread_id,
                                     index_of_last_file_path_in_project)


def go_down_to_project_frame(application=wingapi.gApplication):
    '''
    Go down one frame in the debugger, skipping any non-project frames.

    Did you ever have Wing stop on an exception, and then drop you in code that
    belongs to an external module? This is often annoying, because you want to
    figure out what you did wrong on *your* code, and the external module is
    usually not to blame.

    `go-down-to-project-frame` to the rescue! Invoke this script while
    debugging in order to be taken to the closest lower stack frame that's on a
    project file rather than an external module.

    Suggested key combination: `Alt-F12`
    '''
    project = application.GetProject()
    debugger = application.GetDebugger()
    all_project_files = set(map(_normalize_path, project.GetAllFiles()))
    _current_run_state = debugger.GetCurrentRunState()
    _thread_id, (_, _frame_index) = _current_run_state.GetStackIndex()
    _stack = _current_run_state.GetStack()

    if not _stack:
        return

    file_paths = [_normalize_path(file_path) for file_path, _, _, _, _ in
                  _stack]
    file_paths_in_project_below_current_frame = tuple(
        filter(
            lambda i_and_file_path: i_and_file_path[1] in all_project_files and
                                                                  i_and_file_path[0] > _frame_index,
            enumerate(file_paths)
        )
    )
    if not file_paths_in_project_below_current_frame:
        return
    index_of_last_file_path_in_project = \
                               file_paths_in_project_below_current_frame[0][0]

    _current_run_state.SetStackIndex(_thread_id,
                                     index_of_last_file_path_in_project)


def _available(application=wingapi.gApplication):
    ''' '''
    debugger_run_state = \
                        wingapi.gApplication.GetDebugger().GetCurrentRunState()
    return bool(debugger_run_state and debugger_run_state.GetStack())

go_up_to_project_frame.available = _available
go_down_to_project_frame.available = _available

