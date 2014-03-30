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

base_escape_map = {
    '\\': '\\\\',
    '\'': '\\\'',
    '\"': '\\\"',
    '\a': '\\\a',
    '\b': '\\\b',
    '\f': '\\\f',
    '\n': '\\\n',
    '\r': '\\\r',
    '\t': '\\\t',
    '\v': '\\\v',
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
    formatted = repr(string)
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
    if not ast.literal_eval(formatted_string) == string:
        raise Exception
    return formatted
    


def enter_string():
    app = wingapi.gApplication
    from guiutils import wgtk
    from guiutils import dialogs    
    items = wgtk.VBox()

    entry = wgtk.TextView()
    items.add(entry)

    def ok():
        pass

    button_spec = [
        dialogs.CButtonSpec("_OK", ok),
        dialogs.CButtonSpec("_Cancel", None)
    ]
    title = "Test dialog"

    dlg = dialogs.CWidgetDialog(None, 'my-dialog', title, items, button_spec)
    dlg.Show()    

    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    selection_start, selection_end = editor.GetSelection()
    document.DeleteChars(selection_start, selection_end-1)
    formatted_string = format_string(string)
    document.InsertChars(selection_start, formatted_string)
    new_selection = selection_start + len(formatted_string)
    editor.SetSelection(new_selection, new_selection)
    
    
#enter_string.arginfo = lambda: \
    #{
        #'string': wingapi.CArgInfo(
            #label='String',
            #type=wingutils.datatype.CType(''),
            #formlet=guiutils.formbuilder.CLargeTextGui(allow_newlines=True),
            #doc=''
        #),
    #}

##enter_string.plugin_override = True
#enter_string.label = 'Enter string'
#enter_string.flags = {'force_dialog_argentry': 1}

edit_string = enter_string



import wingapi
import guiutils
import wingutils

def test_aaa(string):
    pass

test_aaa.arginfo = lambda: \
    {
        'string': wingapi.CArgInfo(
            label='String',
            type=wingutils.datatype.CType(''),

formlet=guiutils.formbuilder.CLargeTextGui(allow_newlines=True),
            doc=''
        ),
    }
test_aaa.flags = {'force_dialog_argentry': 1}