# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import with_statement

import os.path, sys
sys.path += [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'third_party.zip'),
    os.path.join(os.path.dirname(__file__), f'third_party_{os.name}.zip'),
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
stripping_pattern = re.compile(r'^(?P<pre_content>\s*)'
                               r'(P<content>.*?)(P<post_content>\s*)')

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


def format_string(string, double=False, triple=False, bytes_=False, raw=False,
                  f_string=False, unicode_=False, avoid_multiline=False,
                  docstring_style=False, starting_column=None):
    if not avoid_multiline:
        assert starting_column is not None
    # if docstring_style:
        # assert triple is True
    assert bytes_ + unicode_ in (0, 1)
    assert f_string + unicode_ in (0, 1)
    quote_character = '"' if double else "'"
    quote_string = quote_character * (3 if triple else 1)
    last_column = \
        wingapi.gApplication.GetPreference('edit.text-wrap-column') - 1

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

    def wrap_content(content):
        return '%s%s%s%s' % (
            ''.join((
                ('f' if f_string else ''),
                ('b' if bytes_ else ''),
                ('u' if unicode_ else ''),
                ('r' if raw else ''),
            )),
            quote_string,
            content,
            quote_string
        )

    formatted_string = wrap_content(content)

    if not avoid_multiline and \
                       (starting_column + len(formatted_string) > last_column):
        # Splitting the string to a multiline one.
        segment_length = last_column - starting_column - \
                 len(quote_string) * 2 - sum(map(int, (bytes_, f_string,
                                                       unicode_, raw)))
        content_segments = [content]
        while True:
            last_content_segment = content_segments[-1]
            if len(last_content_segment) <= segment_length:
                break
            rfind_result = last_content_segment.rfind(' ', 0, segment_length)
            if rfind_result == -1:
                place_to_cut = segment_length
                # This might cut something important but we'll cross that
                # bridge when we get to it.
            else:
                place_to_cut = rfind_result
            del content_segments[-1]
            content_segments.append(last_content_segment[:place_to_cut+1])
            content_segments.append(last_content_segment[place_to_cut+1:])


        separator = ('\n%s' % (' ' * (starting_column)))
        formatted_string = separator.join(
            map(wrap_content, content_segments)
        )
    # elif docstring_style:
        # formatted_string.replace('\\n', '\n')


    #if isinstance(formatted_string, unicode):
        #formatted_string = formatted_string.encode()
    formatted_string_without_f = (formatted_string.replace('f', '', 1) if
                                  f_string else formatted_string)
    if not ast.literal_eval('(%s)' % formatted_string_without_f) == string:
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


def edit_string():
    '''
    Open a dialog for editing a string.

    If the caret is standing on a string, it'll edit the current string.
    Otherwise you can enter a new string and it'll be inserted into the
    document. The dialog has lots of checkboxes for toggling things about the
    string: Whether it's unicode, raw, bytes, f-string, type of quote, etc.

    When is this better than editing a string in the editor?

     - When you have a mess of escape character. The dialog automatically
       translates the escape characters for you so you don't have to think
       about them. (Very useful when entering Windows paths that have
       backslashes in them.)

     - When you're editing a multiline string of this style:
        raise Exception("There's some long text here that takes up more than "
                        "one line, and it's broken in a nice way that doesn't "
                        "exceed 79 characters, and every time you edit it you "
                        "see it as one block of text, while the cutting "
                        "points will be automatically determined by the "
                        "dialog.")

    Note: Currently doesn't work on docstrings, and other triple-quote
    multiline strings.

    Suggested key combination: `Ctrl-Alt-S`

    '''
    app = wingapi.gApplication
    editor = app.GetActiveEditor()
    document = editor.GetDocument()
    last_column = \
                wingapi.gApplication.GetPreference('edit.text-wrap-column') - 1

    selection_start, selection_end = shared.get_selection_unicode(editor)
    selection_start_line = document.GetLineNumberFromPosition(selection_start)
    selection_start_column = selection_start - \
                                    document.GetLineStart(selection_start_line)
    selection_end_line = document.GetLineNumberFromPosition(selection_end)
    selection_end_column = selection_end - \
                                      document.GetLineStart(selection_end_line)

    widget = guiutils.wgtk.QWidget()
    layout = guiutils.wgtk.QVBoxLayout()
    widget.setLayout(layout)
    text_edit_label = guiutils.wgtk.QLabel('&Text:')
    text_edit = guiutils.wgtk.QTextEdit()
    text_edit_label.setBuddy(text_edit)
    sub_layout = guiutils.wgtk.QHBoxLayout()
    bytes_checkbox = guiutils.wgtk.QCheckBox('&Bytes')
    f_string_checkbox = guiutils.wgtk.QCheckBox('&F-string')
    unicode_checkbox = guiutils.wgtk.QCheckBox('&Unicode')
    raw_checkbox = guiutils.wgtk.QCheckBox('&Raw')
    double_checkbox = guiutils.wgtk.QCheckBox('&Double')
    triple_checkbox = guiutils.wgtk.QCheckBox('Tri&ple')
    avoid_multiline_checkbox = guiutils.wgtk.QCheckBox('Avoid &multilne')
    # docstring_style_checkbox = guiutils.wgtk.QCheckBox('D&ocstring style')
    checkboxes = (
        bytes_checkbox, f_string_checkbox, unicode_checkbox, raw_checkbox,
        double_checkbox, triple_checkbox, avoid_multiline_checkbox
    )
    for checkbox in checkboxes: # docstring_style_checkbox):
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
        old_string_raw = document.GetText()[old_string_ranges[0][0] : old_string_ranges[-1][1]]
        old_string = ast.literal_eval('(%s)' % old_string_raw)
        modifiers = string_head_pattern.match(old_string_raw). \
                                                     group('modifiers').lower()
        quote = string_head_pattern.match(old_string_raw).group('quote')
        bytes_checkbox.setCheckState(_bool_to_qt_check_state('b' in modifiers))
        f_string_checkbox.setCheckState(_bool_to_qt_check_state('f' in modifiers))
        unicode_checkbox.setCheckState(_bool_to_qt_check_state('u' in modifiers))
        raw_checkbox.setCheckState(_bool_to_qt_check_state('r' in modifiers))
        double_checkbox.setCheckState(_bool_to_qt_check_state('"' in quote))
        triple_checkbox.setCheckState(_bool_to_qt_check_state(len(quote) == 3))
        avoid_multiline_checkbox.setCheckState(
            _bool_to_qt_check_state((len(old_string_ranges) == 1) and
                                                   selection_end_column > last_column)
        )
        # is_docstring_style = ((set(old_string_raw[-3:]) in ({'"', '"'})) and
                              # ('\n' in old_string_raw))
        # docstring_style_checkbox.setCheckState(
            # _bool_to_qt_check_state(is_docstring_style)
        # )
        # if is_docstring_style:
            # pre_content, old_string, post_content = \
                                   # stripping_pattern.match(old_string).groups()

        # else:
            # pre_content = post_content = None

        string_starting_column = (
            old_string_ranges[0][0] -
            document.GetLineStart(
                document.GetLineNumberFromPosition(old_string_ranges[0][0])
            )
        )

        text_edit.setPlainText(old_string)
    else:
        string_starting_column = selection_start_column

    def ok():
        try:
            string = text_edit.toPlainText()
            bytes_ = bool(bytes_checkbox.checkState())
            f_string = bool(f_string_checkbox.checkState())
            unicode_ = bool(unicode_checkbox.checkState())
            raw = bool(raw_checkbox.checkState())
            double = bool(double_checkbox.checkState())
            triple = bool(triple_checkbox.checkState())
            avoid_multiline = bool(avoid_multiline_checkbox.checkState())
            # docstring_style = bool(docstring_style_checkbox.checkState())

            formatted_string = format_string(
                string, bytes_=bytes_, f_string=f_string, unicode_=unicode_,
                raw=raw, double=double, triple=triple,
                avoid_multiline=avoid_multiline,
                starting_column=string_starting_column,
                # docstring_style=docstring_style
            )
            with shared.UndoableAction(document):
                if replacing_old_string:
                    document.DeleteChars(old_string_ranges[0][0],
                                         old_string_ranges[-1][1] - 1)
                    document.InsertChars(old_string_ranges[0][0],
                                         formatted_string)
                    new_selection_start = old_string_ranges[0][0]
                    new_selection_end = \
                                    new_selection_start + len(formatted_string)
                else:
                    document.DeleteChars(selection_start, selection_end-1)
                    document.InsertChars(selection_start, formatted_string)
                    new_selection_start = new_selection_end = \
                                        selection_start + len(formatted_string)
                shared.set_selection_unicode(editor, new_selection_start,
                                    new_selection_end)
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
