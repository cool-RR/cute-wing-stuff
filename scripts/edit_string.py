# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]

import ast
import collections

import wingapi
import wingutils.datatype
import guiutils.formbuilder

import shared
import string_selecting


#string_head_pattern = re.compile('')

base_escape_map = {
    '\\': '\\\\',
    '\'': '\\\'',
    '\"': '\\\"',
    '\a': '\\a',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
    '\v': '\\v',
}

def escape_character(c, double_quotes, triple_quotes, raw):
    if ((c in ('"', "'")) and triple_quotes) or \
              (c == '"' and not double_quotes) or (c == "'" and double_quotes):
        return c
    elif c in base_escape_map:
        return base_escape_map[c]
    else:
        return c
    

def format_string(string, double_quotes=False, triple_quotes=False,
                  binary=False, raw=False, unicode_=False):
    assert binary + unicode_ in (0, 1)
    quote_string = \
                  ('"' if double_quotes else "'") * (3 if triple_quotes else 1)
    escape_character_ = lambda character: escape_character(
        character, double_quotes=double_quotes, triple_quotes=triple_quotes, 
        raw=raw
    )
    content = ''.join(map(escape_character_, string))
    
    formatted_string = '%s%s%s%s' % (
        ''.join((
            ('b' if binary else ''),
            ('r' if raw else ''),
            ('u' if unicode_ else ''),
        )),
        quote_string,
        content,
        quote_string
    )
    #if isinstance(formatted_string, unicode):
        #formatted_string = formatted_string.encode()
    if not ast.literal_eval(formatted_string) == string:
        raise Exception('Formatting unsuccessful: @%s@  |||  @%s@  ||| @%s@'
              % (string, ast.literal_eval(formatted_string), formatted_string))
    return formatted_string
    


def enter_string():
    app = wingapi.gApplication
    from guiutils import wgtk
    from guiutils import dialogs    

    w = wgtk.QTextEdit()

    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    selection_start, selection_end = editor.GetSelection()
    
    replacing_old_string = \
        string_selecting._is_position_on_strict_string(editor, selection_start)
    if replacing_old_string:
        old_string_start, old_string_end = \
           string_selecting._find_string_from_position(editor, selection_start)
        old_string = ast.literal_eval(
            document.GetCharRange(old_string_start, old_string_end)
        )
        w.setText(old_string)
    
    def ok():
        string = w.toPlainText()
        formatted_string = format_string(string)
        if replacing_old_string:
            document.DeleteChars(old_string_start, old_string_end)
            document.InsertChars(old_string_start, formatted_string)
            new_selection = old_string_start + len(formatted_string)
        else:
            document.DeleteChars(selection_start, selection_end-1)
            document.InsertChars(selection_start, formatted_string)
            new_selection = selection_start + len(formatted_string)
        editor.SetSelection(new_selection, new_selection)
    buttons = [
        dialogs.CButtonSpec("_OK", ok),
        dialogs.CButtonSpec("_Cancel", None),
    ]
    dlg = dialogs.CWidgetDialog(None, 'Edit string', 'Edit string', w, buttons)
    dlg.RunAsModal()    
    
    