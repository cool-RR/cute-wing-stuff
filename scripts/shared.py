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
    editor.ExecuteCommand('backward-word')
    editor.ExecuteCommand('forward-word')
    editor.ExecuteCommand('backward-word')
    editor.ExecuteCommand('forward-word-extend')