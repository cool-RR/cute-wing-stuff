import os

import wingapi, guiutils
from guiutils import winmgr


def switch_to_english():
    print(guiutils.__file__)
    if switch_to_english.on:
        os.system('ping google.com')
    switch_to_english.on = False
    
switch_to_english.on = True


winmgr.CWindowController.class_connect('focus-in', switch_to_english)
