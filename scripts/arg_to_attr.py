import wingapi

def arg_to_attr(editor=wingapi.kArgEditor):
    assert isinstance(editor, wingapi.CAPIEditor)
    document = editor.GetDocument()
    assert isinstance(document, wingapi.CAPIDocument)
    document.BeginUndoAction()
    try:
        #text = document.GetText()
        document.SetText(str(editor.GetSelection()))
    finally:
        document.EndUndoAction()
        
