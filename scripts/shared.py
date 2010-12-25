import re

import wingapi

class UndoableAction(object):
    def __init__(self, document):
        assert isinstance(document, wingapi.CAPIDocument)
        self.document = document
    def __enter__(self):
        self.document.BeginUndoAction()
    def __exit__(self, *args, **kwargs):
        self.document.EndUndoAction()
        
        
def select_current_word(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument
    assert isinstance(document, wingapi.CAPIDocument)
    editor.ExecuteCommand('backward-word')
    start, _ = editor.GetSelection()
    assert start == _
    length = 0
    while length < 1000:
        character = document.GetCharRange(start + length + 1,
                                          start + length + 1)
        if character.isalnum() or character == '_':
            continue
        else:
            break
    end = start + length
    editor.SetSelection(start, end)
    return start, end


def camel_case_to_lower_case(s):
    '''
    Convert a string from camel-case to lower-case.
    
    Example: `camel_case_to_lower_case('HelloWorld') == 'hello_world'`
    '''
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s).\
           lower().strip('_')


def lower_case_to_camel_case(s):
    assert isinstance(s, basestring)
    s = s.capitalize()
    while '_' in s:
        head, tail = s.split('_', 1)
        s = head + tail.capitalize()
    return s