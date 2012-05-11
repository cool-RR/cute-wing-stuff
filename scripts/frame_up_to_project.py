# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `frame_up_to_project` script.

See its documentation for more information.
'''

from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared


def frame_up_to_project():
    
    application = wingapi.gApplication
    project = application.GetProject()
    debugger = application.GetDebugger()
    all_project_files = project.GetAllFiles()
    _current_run_state = debugger.GetCurrentRunState()
    _thread_id, _frame_index = _current_run_state.GetStackFrame()
    _stack = _current_run_state.GetStack()
    
    file_paths = [file_path for file_path, _, _, _, _ in
                  stack[:_stack_frame+1]]
    
    file_paths_in_project = filter(
        lambda _, file_path: file_path in all_project_files,
        enumerate(file_paths)
    )
    
    if not file_paths_in_project:
        return 
    index_of_last_file_path_in_project = file_paths_in_project[-1][0]
    
    _current_run_state.SetStackFrame(_thread_id,
                                     index_of_last_file_path_in_project)
    