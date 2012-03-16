# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `start_debug_with_preset_args` script.

See its documentation for more information.
'''

from __future__ import division
from __future__ import with_statement

import os.path, sys; sys.path.append(os.path.dirname(__file__))

import wingapi

import shared

    
def start_debug_with_preset_args(i_preset=0,
                                 project=wingapi.kArgProject):
    '''
    Start debugging with preset arguments.
    
    You need to have a git-ignored file `cute_wing_stuff_local_settings.py`
    right in this `scripts` folder, which defines a `dict` like this:
    
        all_debug_argument_presets = {
            'my_django_app.wpr': ['runserver --noreload', 'test']
            'other_django_app.wpr': ['runserver 80 --noreload', 'test',
                                     'syncdb']
            None: ['runserver 80 --noreload', 'test'], 
        }
       
    What does this file mean? For each of your projects, you define the
    different presets for debug arguments that will be used for your main debug
    file. `None` is used as the default for any Wing projects that are not
    listed.
    
    Then you call this `start-debug-with-preset-args` with the `i_preset`
    argument equal to the preset index number, and debug will start with those
    arguments.
    '''
    assert isinstance(project, wingapi.CAPIProject)
    
    try:
        import cute_wing_stuff_local_settings
    except ImportError:
        raise Exception('You must have a `cute_wing_stuff_local_settings.py` '
                        'module for this to work.')
    
    ### Determining which presets to use: #####################################
    #                                                                         #
    project_filename = os.path.split(project.GetFilename())[1]
    print (project_filename)
    if project_filename in \
                     cute_wing_stuff_local_settings.all_debug_argument_presets:
        print (0)
        debug_argument_presets = cute_wing_stuff_local_settings. \
                                   all_debug_argument_presets[project_filename]
    else:
        print (1)
        debug_argument_presets = cute_wing_stuff_local_settings. \
                                               all_debug_argument_presets[None]
    #                                                                         #
    ### Finished determining which presets to use. ############################
    
    main_debug_file = project.GetMainDebugFile()
    arguments = debug_argument_presets[i_preset]
    project.SetRunArguments(main_debug_file, arguments)
    wingapi.gApplication.ExecuteCommand('debug-kill')
    wingapi.gApplication.ExecuteCommand('debug-continue')
    