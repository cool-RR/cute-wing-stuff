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
    
    print (vars(debugger.GetRunStates()[0]))
    return 
    #all_project_files = project.GetAllFiles()
    
    
    
    #def _are_we_in_project_frame():
        #''' '''
        #wingapi.gApplication
        
    #while application.CommandAvailable('frame-up') and \
                                                #not _are_we_in_project_frame():
        
    #frame_up_to_project
    #ExecuteCommand('frame-show')
    
    #ExecuteCommand('beginning-of-line-text')
    
    