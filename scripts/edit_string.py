# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__), 
    os.path.join(os.path.dirname(__file__), 'third_party.zip'), 
]

import ast
import re
import collections

import wingapi
import wingutils.datatype
import guiutils.formbuilder
import guiutils.wgtk
import guiutils.dialogs

import shared
import string_selecting


string_head_pattern = re.compile('''^(?P<modifiers>(?:b|u|)r?)'''
                                 '''(?P<quote>\'(?:\'\')?|\"(?:\"\")?)''',
                                 re.I)

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


def format_string(string, double=False, triple=False,
                  bytes_=False, raw=False, unicode_=False,
                  avoid_multiline=False, starting_column=None):
    if not avoid_multiline:
        assert starting_column is not None
    assert bytes_ + unicode_ in (0, 1)
    quote_character = '"' if double else "'"
    quote_string = quote_character * (3 if triple else 1)
    
    if raw and string.endswith(quote_character):
        raise Exception("Can't do a raw string that ends with its quote "
                        "character.")
    
    content_list = []
        
    i = 0
    while i < len(string):
        if triple and string.startswith(quote_string, i):
            content_list.append('\\%s' % quote_string)
            i += 3
            continue
        elif triple and (i == len(string) - 1) and string[i] == quote_string[0]:
            content_list.append('\\%s' % quote_string[0])
            i += 1
            continue # Will now end loop because we're at end of string
        else:
            current_substring = string[i]
            i += 1

        if ((current_substring in ('"', "'")) and triple) or \
                                 (current_substring == '"' and not double) or \
                                         (current_substring == "'" and double):
            content_list.append(current_substring)
        elif current_substring in base_escape_map and not raw:
            content_list.append(base_escape_map[current_substring])
        else:
            content_list.append(current_substring)
            
    content = ''.join(content_list)
    
    formatted_string = '%s%s%s%s' % (
        ''.join((
            ('b' if bytes_ else ''),
            ('u' if unicode_ else ''),
            ('r' if raw else ''),
        )),
        quote_string,
        content,
        quote_string
    )
    #if isinstance(formatted_string, unicode):
        #formatted_string = formatted_string.encode()
    if not ast.literal_eval(formatted_string) == string:
        raise Exception('Formatting unsuccessful. Tried to format this:\r\n'
                        '%s\r\n'
                        '\r\n'
                        'The algorithm come up with this:\r\n'
                        '%s\r\n'
                        '\r\n'
                        'Which actually comes out as a different string, '
                                                           'which is this:\r\n'
                        '%s\r\n'
              % (string, formatted_string, ast.literal_eval(formatted_string), ))
    return formatted_string
    

def _bool_to_qt_check_state(bool_):
    return guiutils.wgtk.Qt.Checked if bool_ else guiutils.wgtk.Qt.Unchecked

# def shit_print(s):
    # open('c:\\tits.txt', 'a').write(s)
    

def edit_string():
    app = wingapi.gApplication
    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    last_column = wingapi.gApplication.GetPreference('edit.text-wrap-column')
    
    selection_start, selection_end = editor.GetSelection()
    starting_line = document.GetLineNumberFromPosition(selection_start)
    starting_column = selection_start - document.GetLineStart(selection_start)
    ending_line = document.GetLineNumberFromPosition(selection_end)
    ending_column = selection_end - document.GetLineStart(selection_end)
    
    widget = guiutils.wgtk.QWidget()
    layout = guiutils.wgtk.QVBoxLayout()
    widget.setLayout(layout)
    text_edit_label = guiutils.wgtk.QLabel('&Text:')
    text_edit = guiutils.wgtk.QTextEdit()
    text_edit_label.setBuddy(text_edit)
    sub_layout = guiutils.wgtk.QHBoxLayout()
    bytes_checkbox = guiutils.wgtk.QCheckBox('&Bytes')
    unicode_checkbox = guiutils.wgtk.QCheckBox('&Unicode')
    raw_checkbox = guiutils.wgtk.QCheckBox('&Raw')
    double_checkbox = guiutils.wgtk.QCheckBox('&Double')
    triple_checkbox = guiutils.wgtk.QCheckBox('Tri&ple')
    avoid_multiline_checkbox = guiutils.wgtk.QCheckBox('Avoid &multilne')
    for checkbox in (bytes_checkbox, unicode_checkbox, raw_checkbox,
                     double_checkbox, triple_checkbox, avoid_multiline_checkbox):
        sub_layout.addWidget(checkbox)
    layout.addWidget(text_edit_label)
    layout.addWidget(text_edit)
    layout.addLayout(sub_layout)
    
    replacing_old_string = \
        string_selecting._is_position_on_string(editor, selection_start)
    if replacing_old_string:
        old_string_ranges = \
           string_selecting._find_string_from_position(editor, selection_start,
                                                       multiline=True)
        old_string_raw = document.GetCharRange(old_string_ranges[0][0],
                                               old_string_ranges[-1][1])
        old_string = ast.literal_eval('(%s)' % old_string_raw)
        modifiers = string_head_pattern.match(old_string_raw). \
                                                     group('modifiers').lower()
        quote = string_head_pattern.match(old_string_raw).group('quote')
        bytes_checkbox.setCheckState(_bool_to_qt_check_state('b' in modifiers))
        unicode_checkbox.setCheckState(_bool_to_qt_check_state('u' in modifiers))
        raw_checkbox.setCheckState(_bool_to_qt_check_state('r' in modifiers))
        double_checkbox.setCheckState(_bool_to_qt_check_state('"' in quote))
        triple_checkbox.setCheckState(_bool_to_qt_check_state(len(quote) == 3))
        avoid_multiline_checkbox.setCheckState(
            _bool_to_qt_check_state((len(old_string_ranges) == 1) and
                                                   ending_column > last_column)
        )
        text_edit.setText(old_string)
        
    def ok():
        try:
            string = text_edit.toPlainText()
            bytes_ = bool(bytes_checkbox.checkState())
            unicode_ = bool(unicode_checkbox.checkState())
            raw = bool(raw_checkbox.checkState())
            double = bool(double_checkbox.checkState())
            triple = bool(triple_checkbox.checkState())
            avoid_multiline = bool(avoid_multiline_checkbox.checkState())
            formatted_string = format_string(
                string, bytes_=bytes_, unicode_=unicode_, raw=raw,
                double=double, triple=triple, avoid_multiline=avoid_multiline,
                starting_column=starting_column
            )
            with shared.UndoableAction(document):
                if replacing_old_string:
                    document.DeleteChars(old_string_ranges[0][0],
                                         old_string_ranges[-1][1] - 1)
                    document.InsertChars(old_string_ranges[0][0],
                                         formatted_string)
                    new_selection = \
                                old_string_ranges[0][0] + len(formatted_string)
                else:
                    document.DeleteChars(selection_start, selection_end-1)
                    document.InsertChars(selection_start, formatted_string)
                    new_selection = selection_start + len(formatted_string)
                editor.SetSelection(new_selection, new_selection)
        except Exception as exception:
            app.ShowMessageDialog('Error', str(exception),
                                  buttons=[('_OK', None)])
            return True
    buttons = [
        guiutils.dialogs.CButtonSpec('_OK', ok),
        guiutils.dialogs.CButtonSpec('_Cancel', None),
    ]
    dialog = guiutils.dialogs.CWidgetDialog(None, 'Edit string',
                                            'Edit string', widget, buttons)
    dialog.RunAsModal()    
    