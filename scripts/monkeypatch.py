# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.


from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
]


import string as string_module
import sys
import os
import inspect

import wingapi
import guiutils.widgets_qt4
import wingide
import cache.textcache

import shared


_ignore_scripts = True

# Must set `monkeypatch = True` in `cute_wing_stuff_local_settings.py` for this
# module to work!

try:
    import cute_wing_stuff_local_settings
except ImportError:
    monkeypatch = False
else:
    monkeypatch = cute_wing_stuff_local_settings.monkeypatch


if monkeypatch:

    ###########################################################################

    # Todo: Perhaps remove this when Wing learns to kill all debug processes
    # when launching a named entry point.

    import debug.client.cmdmanager

    old_debug_named_entry_point = \
              debug.client.cmdmanager.CDebuggerCommands.debug_named_entry_point
    def debug_named_entry_point(self, name):
        """Debug the named entry point"""
        #######################################################################
        #                                                                     #
        # Added part:
        self.debug_kill_all()
        #                                                                     #
        #######################################################################
        return old_debug_named_entry_point(self, name)

    debug.client.cmdmanager.CDebuggerCommands.debug_named_entry_point = \
                                                        debug_named_entry_point


    ###########################################################################

    def _get_location_path(location):
        from wingbase import location as location_module
        if sys.platform == 'win32':
            return location._fOSName
        else:
            return location._fOSName.encode(
                location_module.kFileSystemEncoding
            )


    def _open(self, filenames):
        from wingide.topcommands import location, logging, prefs

        # Get file location object
        loc_list = [location.CreateFromName(name) for name in filenames]

        for loc in loc_list:
            def do_open(abort, loc=loc):
                if abort:
                    msg = (_("File open failed") + '::'
                           + _("Remote file %s could not be inspected.") %
                           self.fGuiMgr.NameForLocation(loc, tstyle='prepend-fullpath use-tilde'))
                    logger = logging.getLogger('editor')
                    logger.error(msg)
                elif loc.IsDirectory():
                    path = _get_location_path(loc)
                    shared.open_folder_in_explorer(path)
                else:
                    opened = False

                    # If so configured, open any project as a project if possible; if fail
                    # to do so, then open it as text
                    if not self.fGuiMgr.fPrefMgr.GetValue(prefs.kOpenProjectsAsText):
                        parts = loc.fUrl.split('.')
                        if parts[-1] == 'wpr' or parts[-1] == 'wpu':
                            self.fSingletons.fWingIDEApp.fProjMgr.OpenProject(loc)
                            opened = True

                    if not opened:
                        # Open the file into active document window
                        win = self.fGuiMgr.GetActiveDocumentWindow()
                        src_text = self.fGuiMgr.DisplayDocument(loc, blank_if_not_found=True,
                                                    win=win, sticky=True)
            loc._WaitForInspect(do_open)


    wingide.topcommands.CApplicationControlCommands._open = _open

    ###########################################################################

    def set_perspective_nicely(*args, **kwargs):
        computer_name = os.environ['COMPUTERNAME'].lower()
        if computer_name == 'turing':
            perspective_name = 'Turing'
        elif computer_name == 'hopper':
            if shared.get_n_monitors() == 2:
                perspective_name = 'Samsung'
            else:
                perspective_name = 'Hopper'
        elif computer_name == 'tardos':
            perspective_name = 'Tardos'
        else:
            # Default
            perspective_name = 'Turing'

        wingapi.gApplication.ExecuteCommand('perspective-restore',
                                            name=perspective_name)

        if shared.autopy_available:
            wingapi.gApplication.InstallTimeout(
                3000 if computer_name == 'hopper' else 1500,
                lambda: autopy.key.tap(
                    'q',
                    [autopy.key.Modifier.ALT, autopy.key.Modifier.META]
                )
            )
            wingapi.gApplication.InstallTimeout(
                3000 if computer_name == 'hopper' else 1500,
                lambda: autopy.key.tap(
                    'w',
                    [autopy.key.Modifier.ALT, autopy.key.Modifier.META]
                )
            )



    # wingapi.gApplication.connect(
        # 'project-open',
        # lambda _: wingapi.gApplication.InstallTimeout(0,
                                                      # set_perspective_nicely)
    # )

    ###########################################################################


    def analyze_text_modified(*args):
        flag, text = args[3:5]
        if flag == 2 and text[-1] in string_module.whitespace:
            shared.clip_ahk()

    cache.textcache.CTextCache.class_connect('text-modified',
                                             analyze_text_modified)


    #######################################################################

    import singleton

    commands_to_clip_after = set(
        ['introduce_variable', 'rename_symbol', 'extract_def',
         'arg_to_attr', 'deep_to_var']
    )

    def command_executed(command_manager, command, args):
        if command.name in commands_to_clip_after:
            shared.clip_ahk()

    wingapi.gApplication.fSingletons.fCmdMgr.connect('cmd-executed',
                                                     command_executed)

    #######################################################################

    def args_needed(*args, **kwargs):
        shared.clip_ahk()

    wingapi.gApplication.fSingletons.fCmdMgr.connect('args-needed',
                                                     args_needed)


